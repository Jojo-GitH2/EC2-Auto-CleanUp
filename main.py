from resources import ec2, ebs, eip


def main():
    # ec2.scan_stopped_instances()
    # ebs.cleanup_unattached_volumes()
    eip.check_unattached_ips()




if __name__ == "__main__":
    main()
