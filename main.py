from resources import ec2, ebs, eip
from datetime import datetime


def main():
    datetime_now = datetime.now().strftime("%Y-%m-%d")
    print(f"EC2 Auto CleanUp started at {datetime_now}\n")
    report_filename = f"cleanup_report_{datetime_now}.log"
    print(f"--- Starting Cleanup (Report: {report_filename}) ---")

    ec2_log = ec2.scan_stopped_instances()
    ebs_log = ebs.cleanup_unattached_volumes()
    eip_log = eip.release_unused_ips()

    with open(report_filename, "w") as f:
        f.write(f"AWS Cleanup Report - {datetime_now}\n")
        f.write("=================================\n\n")

        f.write("EC2 INSTANCES:\n")

        if ec2_log:
            for line in ec2_log:
                f.write(f"{line}\n")
        else:
            f.write("No instances processed.\n")
        f.write("\n")

        f.write("EBS VOLUMES:\n")
        if ebs_log:
            for line in ebs_log:
                f.write(f"{line}\n")
        else:
            f.write("No volumes processed.\n")
        f.write("\n")

        f.write("ELASTIC IPS:\n")
        if eip_log:
            for line in eip_log:
                f.write(f"{line}\n")
        else:
            f.write("No Elastic IPs processed.\n")

        print("Cleanup Complete. Report saved.")


if __name__ == "__main__":
    main()
