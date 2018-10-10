#include <iostream>
#include <memory>
#include <vector>
#include <cstdlib>
#include <cstring>
#include <csignal>
#include <unistd.h>
using namespace std;

#define eprintf(format, ...)                             \
    fprintf(stderr, "\x1b[3%dm[%s:%d(%s)]\x1b[m" format, \
        __LINE__ % 6 + 1, __FILE__, __LINE__,            \
        __PRETTY_FUNCTION__, ##__VA_ARGS__)

#define ewatchi(EXPR) eprintf(#EXPR " = %lld\n", (long long)(EXPR));
#define ewatchx(EXPR) eprintf(#EXPR " = %llx\n", (long long)(EXPR));
#define ewatchf(EXPR) eprintf(#EXPR " = %Lf\n", (long double)(EXPR));
#define ewatcha_gen(EXPR, NNN, TYPE, TYPEFIX)                                 \
    {                                                                         \
        eprintf(#EXPR " = [%lld] {\n", (long long)(NNN));                     \
        for (int __i__ = 0; __i__ < NNN; __i__ += 8) {                        \
            for (int __j__ = 0; __j__ < 8 && __i__ + __j__ < NNN; __j__++)    \
                fprintf(stderr, " %" TYPEFIX, (TYPE)((EXPR)[__i__ + __j__])); \
            fprintf(stderr, "\n");                                            \
        }                                                                     \
        fprintf(stderr, "}\n");                                               \
    }
#define ewatcha(EXPR, NNN) ewatcha_gen(EXPR, NNN, long long, "5lld")
#define ewatchax(EXPR, NNN) ewatcha_gen(EXPR, NNN, long long, "17llx")
#define ewatchaf(EXPR, NNN) ewatcha_gen(EXPR, NNN, long double, "10.6Lf")
#define ewatchs(EXPR) eprintf(#EXPR " = %s\n", (const char*)(EXPR));





enum struct T:char { END, INT, PLUS, MINUS, MUL, DIV, LP, RP, ID, ASSIGN, EXIT, UPLUS, STR, UMINUS };

typedef struct Token {
    char* checksum;
    char* str;
    union { //wait, it's a union structure?.
        int size;
        int value;
    };
    T type;
    Token(T type) : type(type) {};
	Token(T type, int value) : value(value), type(type) {

		eprintf("Token v %d %x %#x\n", type, value, str);
	};
	Token(T type, char* str) : checksum(str), str(str), size(strlen(str)), type(type) {
		eprintf("Token %d %s %#x\n", type, str, str);
	};
    ~Token() { if (type == T::ID || type == T::STR) free(str); }
} *pToken;
using sToken = shared_ptr<Token>;

class Lexer {
    int pos;
    string input;
    pToken readId();
    pToken readStr();
    pToken readDigit();
public:
    Lexer(string &input) : pos(0), input(input) {}; //pos is initial str index poi.
    pToken nToken();
};

pToken Lexer::readDigit() { //this function will read until non-digit meet. -- 12345a
    auto i = 0;
    while (isdigit(input[pos])) i = i * 10 + input[pos++] - '0';
    if (i > 256) throw "does not support integer bigger than 256";
    return new Token(T::INT, i); //assign a Token object with Type:INT & value int.
};

pToken Lexer::readId() {
    auto limit = 0;
    auto start = pos;
    while (isalnum(input[pos++])) if (++limit > 256) throw "does not support ID longer than 256"; //id is alphanum less than 256.
    if (!strncmp("exit", input.substr(start, pos--).c_str(), 4)) return new Token(T::EXIT);
    char* str = (char*)calloc(pos - start + 1, 1); //alloc a space for ID str.
    if (!str) throw "Internal Error";
    strncpy(str, input.substr(start, pos).c_str(), pos - start);
    return new Token(T::ID, str); //with a type and a value.
};

pToken Lexer::readStr() {
    auto limit = 0;
    auto start = ++pos; // ++ bypassed the first ".
    while (input[pos++] != '"') if (++limit > 256) throw "does not support string longer than 256";
    --pos;
    char* str = (char*)calloc(pos - start + 1, 1);
    if (!str) throw "Internal Error";
    strncpy(str, input.substr(start, pos - 1).c_str(), pos++ - start);
    return new Token(T::STR, str);
};

pToken Lexer::nToken() { //nextToken?.
    while (input[pos] == ' ') pos++; //space splited.. if space , move on, if not, process.
    if (pos == input.length()) return new Token(T::END); // if reach to the end.
    if (isdigit(input[pos])) return readDigit(); //if meet first digit.
    if (isalpha(input[pos])) return readId(); //if meet first alpha.
    if (input[pos] == '+') return new Token(T::PLUS, input[pos++]);  //
    if (input[pos] == '-') return new Token(T::MINUS, input[pos++]); //
    if (input[pos] == '*') return new Token(T::MUL, input[pos++]);   //
    if (input[pos] == '/') return new Token(T::DIV, input[pos++]);   //
    if (input[pos] == '(') return new Token(T::LP, input[pos++]);    //
    if (input[pos] == ')') return new Token(T::RP, input[pos++]);    //
    if (input[pos] == '"') return readStr(); //meet with string.
    if (input[pos] == '=') return new Token(T::ASSIGN, input[pos++]);
    throw "Lexer Error";
};

struct Node { //Node is sth. contains a token and a children node vector.
    shared_ptr<Token>token;
    vector<shared_ptr<Node>>children;
    Node(sToken token) : token(token) {};
};
using sNode = shared_ptr<Node>;

class Parser {
    shared_ptr<Lexer> lexer; //pointing to a lexer object with input initialized.
    shared_ptr<Token> cur; // assigned with lexer->nToken return value.
    void next(T);
    sNode factor();
    sNode term();
    sNode expr();
    sNode assign();
public:
    Parser(shared_ptr<Lexer> lexer) : lexer(lexer), cur(lexer->nToken()) {};
    sNode parse();
};

void Parser::next(T type) {
    if (cur->type == type) cur.reset(lexer->nToken()); //If cur->type is expected, cur update token.
    else throw "Parser Error";
};

sNode Parser::factor() {
    auto node = make_shared<Node>(cur);
    auto osNode = make_shared<Node>(cur);
    switch (cur->type) {
        case T::LP: //(
            next(T::LP);
            node = expr();
            next(T::RP); //)
        break;
        case T::PLUS:
        case T::MINUS:
            cur->type = cur->type == T::PLUS ? T::UPLUS : T::UMINUS;
            next(cur->type);
            osNode->children.push_back(factor());
            node = osNode;
        break;
        case T::ID:
        case T::INT:
        case T::STR:
        case T::MUL:
        case T::DIV:
        case T::EXIT:
            next(cur->type);
        break;
    };
    return node;
};

sNode Parser::term() {
    auto node = factor();
    while (true) {
        if (cur->type == T::MUL || cur->type == T::DIV) {
            auto osNode = make_shared<Node>(cur);
            next(cur->type);
            osNode->children.push_back(node);
            auto check = factor();
            if (check->token->type == T::END) throw "Parser Error";
            osNode->children.push_back(check);
            node = osNode;
        } else break;
    }
    return node;
};

sNode Parser::expr() {
    auto node = term();
    while (true) {
        if (cur->type == T::PLUS || cur->type == T::MINUS) {
            auto osNode = make_shared<Node>(cur);
            next(cur->type);
            osNode->children.push_back(node);
            auto check = term();
            if (check->token->type == T::END) throw "Parser Error";
            osNode->children.push_back(check);
            node = osNode;
        } else break;
    }
    return node;
};

sNode Parser::assign() {
    auto node = expr();
    while (true) {
        if (cur->type == T::ASSIGN) {
            auto osNode = make_shared<Node>(cur);
            next(cur->type);
            osNode->children.push_back(node);
            auto check = expr();
            if (check->token->type == T::END) throw "Parser Error";
            osNode->children.push_back(check);
            node = osNode;
        } else break;
    }
    return node;
};

sNode Parser::parse() {
    auto result = assign(); // start parsing , finish right if cur->type != T::END
    if (cur->type != T::END) throw "Parser Error";
    return result;
};

static struct Symbol {
    char* id;
    sToken token;
    Symbol* next;
    Symbol(){};
    Symbol(char *str, sToken token) : token(token) {
        id = (char*) calloc(strlen(str) + 1, 1); //Calloc an identifier as Symbol.
        if (!id) throw "Internal Error";
        strcpy(id, str);
    };
} SymTab;

void print(char *s, int n) {
    if (n != fwrite(s, 1, n, stdout)) exit(0);
}

void print(int n) {
    printf("%d", n);
}

void print(sToken result) {
    if (result->checksum != result->str) {
        print((char*)"EXIT", 4);
        exit(0);
    };
    if (result->size > 4) print(result->str, 4);
    else print(result->str, result->size);
}

class Calc {
    sToken visitor(sNode);
    sToken visitUnaryOp(sNode);
    sToken visitBinaryOp(sNode);
    sToken visitId(sNode);
    sToken visitAssign(sNode);
public:
    void interpret(sNode);
};

sToken Calc::visitor(sNode node) {
    switch (node->token->type) {
        case T::EXIT:
            print((char*)"Bye\n", 4);
            exit(0);
        case T::END:
            return node->token;
        case T::INT:
        case T::STR:
            return node->token;
        case T::UPLUS:
        case T::UMINUS:
            return visitUnaryOp(node);
        case T::PLUS:
        case T::MINUS:
        case T::MUL:
        case T::DIV:
            return visitBinaryOp(node);
        case T::ASSIGN:
            return visitAssign(node);
        case T::ID:
            auto check = visitId(node);
            if (!check) throw "Symbol Error";
            return check;
     };
     throw "Syntax Error";
};

sToken Calc::visitUnaryOp(sNode node) {  //Plus or Minus.
    auto result = 0;
    auto op = visitor(node->children[0]);
    if (op->type == T::INT) result = op->value;
    else if(op->type == T::STR) result = atoi(op->str);
    else throw "Syntax Error";
    return make_shared<Token>(T::INT, node->token->type == T::UPLUS ? +op->value : -op->value);
};

sToken Calc::visitBinaryOp(sNode node) { //+,-,*,/
    auto left = 0;
    auto right = 0;
    auto leftToken = visitor(node->children[0]);
    auto rightToken = visitor(node->children[1]);
    if (leftToken->type == T::INT) left = leftToken->value;
    else if(leftToken->type == T::STR) left = atoi(leftToken->str);
    else throw "Syntax Error";
    if (rightToken->type == T::INT) right = rightToken->value;
    else if(rightToken->type == T::STR) right = atoi(rightToken->str);
    else throw "Syntax Error";
    switch (node->token->type) {
        case T::PLUS:return make_shared<Token>(T::INT, left + right);
        case T::MINUS:return make_shared<Token>(T::INT, left - right);
        case T::MUL:return make_shared<Token>(T::INT, left * right);
        case T::DIV:return make_shared<Token>(T::INT, left / right);
    };
    print((char*)"EXIT", 4);
    exit(0);
};

sToken Calc::visitId(sNode node) { // find target id to access.
    sToken result = nullptr;
    auto symbol = &SymTab;
    while (symbol->next != &SymTab) {  //find target Symbol ID until searching the whole linked list.
        symbol = symbol->next;
        if (!strncmp(node->token->str, symbol->id, strlen(symbol->id))) {
            result = symbol->token;
            break;
        }
    };
    return result;
};

sToken Calc::visitAssign(sNode node) {
    auto var = node->children[0]; //This Procedure assign child[1] to child[0].
    auto value = visitor(node->children[1]);
    if (var->token->type != T::ID || !value) throw "Syntax Error";
    if (auto variable = visitId(var)) { // if visited ID exists,
        if (variable->type == T::STR && value->type == T::STR) { // if both string.
            if (variable->size < value->size) variable->str = (char*)realloc(variable->str, value->size + 1);
            if (!variable->str) throw "Internal Error";
            variable->checksum = variable->str;
            variable->size = strlen(variable->str); //wait.. the size hasn't been updated..?
            strcpy(variable->str, value->str);
        } else if (variable->type == T::INT && value->type == T::STR) variable->value = atoi(value->str);
        else variable->value = value->value;
    } else { //create a new variable.
        auto symbol = &SymTab;
        while (symbol->next != &SymTab) symbol = symbol->next;
        symbol->next = new Symbol(var->token->str, value); // a variable is a symbol..
        symbol->next->next = &SymTab;
    }
    return value;
};

void Calc::interpret(sNode AST) {
    auto result = visitor(AST);
    if (result->type == T::INT) print(result->value);
    else print(result);
};

int main() {
    SymTab.next = &SymTab;
    signal(SIGALRM, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    cout << "combabo calculator" << endl;
    sleep(3);
    while (true) {
        string input;
        alarm(0);
        print((char*)">>> ", 4);
        getline(cin, input);
        try {
            shared_ptr<Lexer>lexer(new Lexer(input));
            shared_ptr<Parser>parser(new Parser(lexer));
            shared_ptr<Calc>calc(new Calc());
            calc->interpret(parser->parse());
        } catch(const char *s) {
            print((char*)s, strlen(s));
        }
        alarm(0);
        print((char*)"\n", 1);
    }
    return 0;
}
