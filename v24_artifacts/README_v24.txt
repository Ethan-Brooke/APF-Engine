APF v24 bottom MSbar export-candidate closure

Targeted verifier:
  PYTHONPATH=. python scripts/check_bottom_msbar_export_candidate.py

Filtered verify_all:
  PYTHONPATH=. python verify_all.py --module bottom_msbar_export_candidate --no-scorecard
