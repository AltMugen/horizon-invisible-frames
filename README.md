# Invisible Frames for Horizon

Native server-side feature for Minecraft 26.3 / Horizon, tested on
3db53df3bde39da07aabddec9a5fa850204fd32a with Horizon Mixins
07dab17387480ac03829584d9d1ee9912c9bb515.

Sneak and right-click a **nonempty** item frame or glow frame to hide its frame.
It becomes fixed so ordinary right-clicks do not rotate or remove the displayed
item. Sneak and right-click it again to restore its visibility and unlock it.
Empty visible frames stay visible. A fixed visible frame cannot be unlocked by
a survival player. Breaking the supporting block and creative interactions are
still controlled by the engine. This is not a claim/region-protection system.

The native mod is required on the Horizon server/integrated host. Changes use
vanilla entity metadata, so remote clients do not need the mod's code.

Original MIT implementation of the documented interaction. Inspired by
[InvisibleFrames](https://github.com/ADHDMC/InvisibleFrames); not affiliated.
No source, assets or code from a Java mod are bundled.

Validation details and limitations are in VALIDATION.md. Source files built into
the mod are under mixins/invisible_frames/. Build instructions are in tools/build.py.

## Build

Clone the MIT Horizon and horizon-mixins repositories. Build the latter at the
exact commit in compatibility.json. Then:

```sh
python3 tools/build.py check --horizon /path/to/horizon --mixins-cli /path/to/horizon-mixins --target-dir /path/to/cargo-target
python3 tools/build.py package
```

The build exports the committed Horizon revision and applies the native mixins to
a temporary source tree. It does not launch the game or read player saves.
Development assisted by Codex.
