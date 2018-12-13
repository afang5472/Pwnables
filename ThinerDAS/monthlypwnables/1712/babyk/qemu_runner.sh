#!/bin/sh

set -ve

KERNEL_PATH="bzImage"
INITRD="initramfs-busybox-x86_64.cpio.gz"
QEMU_SYSTEM_X86_64="qemu-system-x86_64"
CPU_SPEC="-enable-kvm -cpu kvm64,+smep"

exec ${QEMU_SYSTEM_X86_64} \
    -kernel ${KERNEL_PATH} \
    -initrd ${INITRD} \
    -nographic -append "console=ttyS0 oops=panic panic=1 quiet kaslr" \
    -m 64M \
    ${CPU_SPEC} \
    -monitor /dev/null \
    -serial /dev/null \
    -serial stdio \
    2>/dev/null
