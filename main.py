import argparse
from app import llm_sim, segment_sim, crypto_sim, cyber_hack, pentest_hack

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["hack", "llm", "cyber", "segment", "crypto"], required=True,
                        help="Select the simulation mode to run, one of: hack, llm, cyber, segment, crypto")
    args = parser.parse_args()

    if args.mode == "hack":
        pentest_hack()
    elif args.mode == "llm":
        llm_sim()
    elif args.mode == "cyber":
        cyber_hack()
    elif args.mode == "segment":
        segment_sim()
    elif args.mode == "crypto":
        crypto_sim()
        
        
if __name__ == "__main__":
    main()