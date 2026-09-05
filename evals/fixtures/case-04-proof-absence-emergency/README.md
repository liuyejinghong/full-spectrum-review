# Position protection maintenance

Managed positions require venue stop coverage. Operators can also install
protection through another system order path. The venue API provides current
open stops and accepts new stop requests. The local proof store may need
reconstruction after restart; venue orders survive that restart.

Domain Packs: trading. This is a source excerpt without git history. The
external `venue` library is outside the snapshot; inspect the caller contract,
not the availability of that dependency.
