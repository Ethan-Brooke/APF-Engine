# Guarded P2M publisher successor

OWNER: Publisher, task 01a07cda-6f8a-7b60-ade8-d01095f3f6a3.
REGEN: AUTHORED; candidate pending independent integration acceptance.
CHECK: The frozen integration manifest, exact installed gate file hashes and independent acceptance.

This is the maintained successor transport to the frozen physical-interface runner's JSON `call` and separate multipart `/verify` branches. The frozen old runners remain historical evidence and are not modified. New scientific writes use `P2MClient.call`, `send_reviewed` or `multipart`; every non-GET call goes through `GuardedPrivatePublisher` on each invocation. Payloads are immutable bytes. The actual callback constructs a urllib Request with those same bytes and opens it once. The final exact-action evidence and expiry check runs after the journal callback and HTTP Request construction, immediately before opener.open in both lanes. Redirects and automatic write retries are disabled. GET and the fixed `/agent/refresh` operation remain separate; importing this module reads no credentials and performs no network activity.

The separate `AdministrativeP2MClient.send_administrative` method uses the independently reviewed administrative gate. The callback obtains the current mission using the actual list endpoint, checks its ID, privacy and exact description projection, revalidates release evidence and expiry after that read, and sends the exact reviewed bytes only on a match. A failed read, changed baseline or expiry during the read prevents the PATCH. There is no server-side compare-and-swap: a different writer could change the mission after the GET. Single-writer coordination remains necessary.

`guarded_publish.py` is the executable entry point for a single reviewed request. Supply the actual gate checkout, exact authorization path and independently communicated hash, assigned publisher ID, method/path/media type, frozen payload, credentials path and an unused journal directory. It preflights before reading credentials or refreshing, then the wrapper validates again for the write. Scientific lane defaults to private_stage; administrative lane defaults to administrative_update. An existing attempt journal prevents blind replay. An uncertain network result requires read-only reconciliation, not another write attempt. A response alone is not delivery completion: read the actual remote object back and compare all intended and protected fields.

For multipart publication, call build_verify_payload with an explicit boundary before independent review and save the resulting bytes. Freeze those exact bytes and content type in the release; multipart sends them directly without generating a new boundary or reserializing them. The current operations assignment does not authorize new proof uploads.

Run offline boundary checks with your Python and actual paths:

    python -B run_tests.py --gate-root <installed-gate-checkout> --fixture-root <accepted-candidate04-tests-directory> --admin-gate-root <administrative-candidate-or-installed-root>

Fixtures contain synthetic evidence, not credentials. The transport opener is captured; no network is contacted. The tests exercise the actual client methods through the real gate to the urllib request boundary. They do not authenticate review identities, certify source meaning, provide platform-wide enforcement, impose a cross-process lock, or demonstrate second-box execution. The scientific gate files are unchanged. Direct clients, private transport methods used outside the entry point, edited implementations, dishonest callbacks and legacy runners remain explicitly outside this boundary.

Per-box authorization records must use actual local evidence paths and an independently trusted authorization hash. Runtime paths are supplied as arguments; no brook-specific path is embedded in the adapter. Shared files do not certify another machine's installation. Independent review, installation, observed use and actual second-box execution remain separate recorded states.
