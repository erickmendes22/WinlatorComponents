# DD Turnip v0.9.1 — Android Bionic with Linux GPU patches

This is an **isolated build recipe** using the exact public source of
[Droid-Deck/Drivers DD-Turnip-v0.9.1](https://github.com/Droid-Deck/Drivers/releases/tag/DD-Turnip-v0.9.1)
and Mesa **0c418c5054a1223668c73614227c5f4cb67addaf**.

The unmodified release applies six core Turnip/IR3 patches **only to Linux**.
`port.py` changes their target selection to `["android", "linux"]` **before**
`scripts/build_android.sh` clones and patches Mesa. It preserves the original
patch order, and retains all original Android IMapper5, UBWC and gralloc patches.

| Integrated into Android | Purpose |
|---|---|
| linux/0001 mesh emulation | VK_EXT_mesh_shader implemented using compute |
| linux/0002 half-wave subgroup | required half-wave subgroup sizes on A8xx |
| linux/0003 cube direction sanitize | protect A8xx cubemap sampling from invalid directions |
| linux/0004 bindless invalidate | A8xx-specific bindless invalidate registers |
| linux/0005 KGSL IB virtual alias | command stream alias to address 32-bit rollover |
| linux/0006 shuffle broadcast | optimized uniform/mixed subgroupShuffle lowering |

**Not directly portable**: `scripts/linux_kgsl_wsi.py` advertises the Linux
DRM/dma-buf device node, which is not Android's KGSL/Android WSI identity.
`scripts/linux_gralloc_exports.py` uses a **DroidDeck compositor** Unix
socket under `$XDG_RUNTIME_DIR`, absent on Android. Android already uses
AHardwareBuffer / IMapper5 / UBWC allocation through its existing patches.
Blindly enabling these two scripts would not integrate an Android equivalent.

## Build

The separate GitHub Actions workflow **builds Android only**, publishes a
root-level Adrenotools ZIP, verifies the ELF is **AArch64 Bionic** and contains
the IMapper5 code path. It does **not** run Linux build or unrelated regression
tests.

For a local build with NDK r26d and normal Mesa build dependencies:

```sh
git clone https://github.com/Droid-Deck/Drivers.git drivers
git -C drivers checkout ac34abe1406645fe18e12db9fe3102ebd2c637d2
python3 dd-turnip-bionic/port.py drivers/patches/series.json
drivers/scripts/fetch_mesa.sh drivers/work/mesa 0c418c5054a1223668c73614227c5f4cb67addaf
drivers/scripts/build_android.sh drivers/work/mesa
python3 dd-turnip-bionic/package.py drivers/out/android/libvulkan_freedreno.so
```

Source patch set is GPL-3.0; all original authors and licenses are retained.
Successful compilation does not alone establish correct rendering on every
A8xx, and functional Vulkan tests are still required on a device.
