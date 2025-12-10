import resources.ec2 as ec2


def main():
    ec2.scan_stopped_instances()


if __name__ == "__main__":
    main()