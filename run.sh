#!/bin/bash

# ==========================
# Colors
# ==========================
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
BLUE="\e[34m"
CYAN="\e[36m"
WHITE="\e[97m"
RESET="\e[0m"

# ==========================
# Banner
# ==========================
show_banner() {
    clear
    echo -e "${CYAN}================================================================================"
    cat << "EOF"
██████╗ ██████╗ ██╗███████╗████████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗██║██╔════╝╚══██╔══╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
██║  ██║██████╔╝██║█████╗     ██║   ██║  ███╗██║   ██║███████║██████╔╝██║  ██║
██║  ██║██╔══██╗██║██╔══╝     ██║   ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
██████╔╝██║  ██║██║██║        ██║   ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝        ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
EOF

    echo
    echo -e "${CYAN}    ╔════════════════════════════════════════════════════════════════════╗${RESET}"
    echo -e "${WHITE}    ║  Terraform Drift Detection • Security Analysis • Compliance Audit  ║${RESET}"
    echo -e "${CYAN}    ╚════════════════════════════════════════════════════════════════════╝${RESET}"
    echo -e "${CYAN}================================================================================"
}

# ==========================
# Menu
# ==========================
show_menu() {
    echo -e "${YELLOW}Select Resource Type:${RESET}"
    echo -e "${GREEN}1.${RESET} EC2 Drift Detection"
    echo -e "${GREEN}2.${RESET} Security Group Drift Detection"
    echo -e "${GREEN}3.${RESET} S3 Drift Detection"
    echo -e "${GREEN}4.${RESET} Exit"
    sleep 1
}

# ==========================
# Choice Handler
# ==========================
get_choice() {
    while true; do
        read -p "Enter your choice [1-4]: " choice

        case $choice in
            1)
                resource="ec2"
                echo -e "\n${GREEN}[INFO] EC2 Drift Detection Selected${RESET}"
                break
                ;;
            2)
                resource="security_group"
                echo -e "\n${GREEN}[INFO] Security Group Drift Detection Selected${RESET}"
                break
                ;;
            3)
                resource="s3"
                echo -e "\n${GREEN}[INFO] S3 Drift Detection Selected${RESET}"
                break
                ;;
            4)
                echo -e "\n${BLUE}[INFO] Exiting DriftGuard...${RESET}"
                exit 0
                ;;
            *)
                echo -e "${RED}[ERROR] Invalid option. Please select 1-4.${RESET}"
                ;;
        esac
    done
}

# ==========================
# Giving tfstate file location
# ==========================
get_tfstate_path() {
    while true; do
        echo
        read -p "Enter Terraform state file path: " tfstate_path

        if [[ ! -f "$tfstate_path" ]]; then
            echo -e "${RED}[ERROR] File does not exist.${RESET}"
            sleep 1
            continue
        fi

        if [[ "$tfstate_path" != *.tfstate ]]; then
            echo -e "${RED}[ERROR] Invalid file. Only .tfstate files are allowed.${RESET}"
            sleep 1
            continue
        fi

        echo -e "${GREEN}[INFO] Valid tfstate file detected.${RESET}"
        break
    done
}

# ==========================
# Main
# ==========================
run_drift_detection() {
    echo
    echo -e "${BLUE}[INFO] Starting Drift Detection Engine...${RESET}"
    echo -e "main.py --resource \"${resource}\" --tfstate \"${tfstate_path}\""

    python3 main.py --resource "$resource" --tfstate "$tfstate_path"
}

# ==========================
# Main
# ==========================
main() {
    show_banner
    echo -e "${BLUE}[INFO] Initializing DriftGuard Engine...${RESET}"
    echo
    show_menu
    get_choice
    get_tfstate_path
    run_drift_detection
}

main
