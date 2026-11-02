# Validation — 2026-11-02

Tested Horizon 3db53df3bde39da07aabddec9a5fa850204fd32a,
Horizon Mixins 07dab17387480ac03829584d9d1ee9912c9bb515, Linux x86-64, Vulkan.

- Native AST apply passed together with the other AltCraft native prototypes.
- The full optimized game and horizon-ctl compiled successfully.
- An actual integrated server was launched with a fresh temporary game home,
  launcher home and XDG folders. No real player worlds were used.
- Shift + ordinary right-mouse input changed a filled item frame to Invisible=1 and Fixed=1,
  verified through the real server's /data get command.
- Repeating the input restored Invisible=0 and Fixed=0.
- Both states were captured in real rendered frames.
- Dedicated servers, protection-mod interoperability and disconnect/restart persistence
  have not been separately exercised in this first release. The engine's persisted frame
  fields are used; there is no separate custom frame save format.
