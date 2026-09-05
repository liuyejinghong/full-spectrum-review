# Risk-triggered position close

The risk handler requests closure of a managed position. Operations must be
able to associate each submitted action and its later fills with the position
and trade that caused it, including after restart. The venue assigns an order
ID on acceptance; acceptance and later execution are separate events.

`on_risk_signal()` owns the complete pre-submission path: callers pass the
position object without persisting action metadata. The venue wrapper forwards
the explicitly supplied arguments and does not inject application identifiers.

Domain Packs: trading. This is a source excerpt without git history. The
external `venue` library is outside the snapshot; inspect the caller contract,
not the availability of that dependency.
