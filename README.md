# AWS EC2 Auto-Cleanup Utility

A Python-based automation tool designed to optimize AWS costs by identifying and cleaning up unused resources. This utility scans for stopped EC2 instances, unattached EBS volumes, and unused Elastic IPs, generating a detailed report of potential cost savings.

## 🚀 Key Features

- **EC2 Instance Cleanup:** Identifies instances that have been stopped for longer than X days.
- **EBS Volume Cleanup:** Finds unattached volumes that have been sitting idle longer than X days.
- **Elastic IP Release:** Detects and releases Elastic IPs that are not associated with any running instance.
- **Safety First:** Includes a `DRY_RUN` mode to simulate actions without deleting resources.
- **Reporting:** Generates a timestamped `.txt` report of all actions taken.

## 🛠️ Tech Stack

- **Language:** Python 3.x
- **SDK:** AWS Boto3
- **Logic:** Custom date-parsing for resource age calculation (Timezone Aware).

## 📂 Project Structure

```text
aws-cleanup-utility/
│
├── main.py                # The entry point (Orchestrator)
├── config.py              # Configuration (Thresholds, Dry Run, Region)
├── requirements.txt       # Dependencies
├── README.md              # Documentation
│
└── resources/             # Logic Modules
    ├── __init__.py
    ├── ec2.py             # EC2 stop-logic
    ├── ebs.py             # EBS orphan-logic
    └── eip.py             # EIP release-logic
```

## ⚙️ Configuration

All settings are managed in `config.py`:

```Python
# config.py

# Set to True to print actions without deleting (Safety Mode)

DRY_RUN = True

# Thresholds (How long a resource must be idle before deletion)

STOPPED_HOURS_THRESHOLD = 24

# AWS Region to scan

AWS_REGION = 'us-east-1'
```

## 🔧 Setup & Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/aws-cleanup-utility.git
   cd aws-cleanup-utility
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Credentials**: Ensure your AWS credentials set up locally
   ```
   aws configure
   ```
4. **Run the Utility:**
   ```bash
   python main.py
   ```
5. **View Report:** Check the generated file (e.g. `cleanup_report_2025-12-12.txt`) for the results

## ⚠️ Safety Mechanism

By default, `DRY_RUN` is set to `True`. This ensures that **no resources are deleted** when you first run the script. The script will only print "Would delete..." to the console and the report.

To enable actual deletion, change `DRY_RUN = False` in `config.py`.

## 🤝 Contribution

Feel free to fork this project and submit pull requests for new features (e.g., Email reporting via SNS, Lambda support).
