#include <algorithm>
#include <cassert>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <queue>
#include <set>
#include <vector>

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

typedef long long ll;
typedef unsigned long long ull;

using std::map;
using std::queue;
using std::set;

const ll INFTY = 0x7fffffffffffffLL;

const char* const NO_STR = "No";
const char* const YES_STR = "Yes";

int poly[5][2][3] = {
    { { 1, 0, 2 }, { 0, 2, 2 } }, //a+2c, 2b+2c
    { { 1, 1, 1 }, { 0, 2, 2 } }, //a+b+c, 2b+2c
    { { 2, 0, 1 }, { 1, 2, 1 } }, //2a+c, a+2b+c
    { { 1, 1, 2 }, { 1, 1, 1 } }, //a+b+2c, a+b+c
    { { 3, 1, 1 }, { 0, 1, 1 } }, //3a+b+c, b+c
};

bool solve_2(int a, int b, int c, int w, int h)
{
    //eprintf("a=%5d, b=%5d, c=%5d, w=%5d, h=%5d\n", a, b, c, w, h);
    int v[3] = { a, b, c };
    for (int i = 0; i < 5; i++) {
        int d[2] = {};
        for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 3; k++) {
                d[j] += poly[i][j][k] * v[k];
            }
        }
        if (d[0] <= w && d[1] <= h)
            goto GOOD;
    }
    return false;
GOOD:
    //eprintf("GOOD!!!\n");
    return true;
}

bool solve_1(int a, int b, int c, int w, int h)
{
    return solve_2(a, b, c, w, h) || solve_2(a, c, b, w, h) || solve_2(b, a, c, w, h) || solve_2(b, c, a, w, h) || solve_2(c, a, b, w, h) || solve_2(c, b, a, w, h);
}

bool solve(int a, int b, int c, int w, int h)
{
    return solve_1(a, b, c, w, h) || solve_1(a, b, c, h, w);
}

int main()
{
    int a, b, c, w, h;
    scanf("%d%d%d%d%d", &a, &b, &c, &w, &h);
    printf("%s\n", solve(a, b, c, w, h) ? YES_STR : NO_STR);
    return 0;
}

/*
//const int PN = 16777216;
const int PN = 1048576;

bool is_nprime[PN];

int prime_list[PN / 4];
int prime_count;

ll gcd(ll a, ll b)
{
    ll c;
    while (b != 0) {
        c = a % b;
        a = b;
        b = c;
    }
    return a;
}

void gen_prime()
{
    memset(is_nprime, 0, sizeof(is_nprime));
    is_nprime[0] = true;
    is_nprime[1] = true;
    for (ll i = 2; i < PN; i++) {
        if (!is_nprime[i]) {
            prime_list[prime_count++] = i;
            for (ll j = i * i; j < PN; j += i) {
                is_nprime[j] = true;
            }
        }
    }
}

ull mulmod_pow2(ull x, ull e, ull N)
{
    // return x*2^e
    x = x % N;
    for (int i = 0; i < e; i++) {
        x = (x << 1);
        if (x >= N)
            x -= N;
    }
    return x;
}

ll addmod(ll x, ll y, ll N)
{
    return (x % N + y % N + 2 * N) % N;
}

ull mulmod(ull x, ull y, ull N)
{
    x = x % N;
    y = y % N;
    ull x1 = x & 0xffffffff;
    ull x2 = (x >> 32) & 0xffffffff;
    ull y1 = y & 0xffffffff;
    ull y2 = (y >> 32) & 0xffffffff;
    return ((x1 * y1) % N + mulmod_pow2(x1 * y2 + x2 * y1, 32, N) + mulmod_pow2(x2 * y2, 64, N)) % N;
}

ll powmod(ll a, ll e, ll N)
{
    if (e == 0)
        return 1;
    if (e == 1)
        return a % N;
    a = a % N;
    ll x = a;
    ll r = 1;
    while (e) {
        if (e & 1)
            r = mulmod(r, x, N);
        e = e >> 1;
        x = mulmod(x, x, N);
    }
    return r;
}

bool is_prime_under(ll p, int i)
{
    ll d = p - 1;
    int o = 0;
    while ((d & 1) == 0) {
        d >>= 1;
        o++;
    }
    ll pp = powmod(i, d, p);
    if (pp == 1 || pp == p - 1)
        return true;
    for (int j = 0; j < o; j++) {
        pp = mulmod(pp, pp, p);
        if (pp == p - 1)
            return true;
        if (pp == 1)
            return false;
    }
    return false;
}

bool is_prime_fast(ll p)
{
    for (int i = 0; i < 10; i++) {
        int pp = prime_list[i];
        if (p == pp) {
            return true;
        }
        if (!is_prime_under(p, pp))
            return false;
    }
    // we dont have more proof ha
    return true;
}

ll my_abs(ll x)
{
    return x > 0 ? x : -x;
}

ll rho(ll n, ll x, ll c)
{
    // c=1,...,n-1
    if (n == 1)
        return n;
    if (n % 2 == 0)
        return 2;
    ll y = x;
    ll d = 1;
    while (d == 1) {
        x = addmod(powmod(x, 2, n), c, n);
        y = addmod(powmod(y, 2, n), c, n);
        y = addmod(powmod(y, 2, n), c, n);
        ll diff = my_abs(x - y);
        d = gcd(diff, n);
        if (d == n)
            return n;
    }
    return d;
}

ll try_div(ll n)
{
    ll st = sqrt(n) + 1;
    int s = std::lower_bound(prime_list, prime_list + 1024, st) - prime_list + 2;

    for (int i = 0; i < s; i++) {
        if (n % prime_list[i] == 0)
            return prime_list[i];
    }
    return n;
}

ll one_factor(ll n)
{
    if (n == 1)
        return 1;
    if (is_prime_fast(n))
        return n;
    ll v = try_div(n);
    if (v != n)
        return v;
    for (ll c = 1; c < n; c += (1 + n / 65536)) {
        ll f = rho(n, 2, c);
        if (f != n) {
            return f;
        }
        f = rho(n, 3, c);
        if (f != n) {
            return f;
        }
        f = rho(n, 5, c);
        if (f != n) {
            return f;
        }
        f = rho(n, 7, c);
        if (f != n) {
            return f;
        }
    }
    return n;
}

std::multiset<ll> factor(ll n, std::multiset<ll> base = std::multiset<ll>())
{
    if (n == 1)
        return base;
    ll f = one_factor(n);
    if (f == n) {
        base.insert(f);
        return base;
    } else {
        return factor(n / f, factor(f, base));
    }
}

const int N = 128;

ll buf[N];
ll times[N];
ll actual[N];
int buf_len;

int main()
{
    gen_prime();
    ll n;
    scanf("%lld", &n);
    std::multiset<ll> vals = factor(n);
    bool first = true;
    for (ll i : vals) {
        if (!first) {
            printf(" ");
        }
        first = false;
        printf("%lld", i);
    }
    printf("\n");
    //    ewatchi(i);
    return 0;
}

*/
