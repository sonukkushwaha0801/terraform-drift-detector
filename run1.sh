#!/bin/bash
show_banner()
{
    clear
    echo "=========================================="
    cat << "EOF"
    ██████╗ ██████╗ ██╗███████╗████████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ ██████╗
    ██╔══██╗██╔══██╗██║██╔════╝╚══██╔══╝██╔════╝ ██║   ██║██╔══██╗██╔══██╗██╔══██╗
    ██║  ██║██████╔╝██║█████╗     ██║   ██║  ███╗██║   ██║███████║██████╔╝██║  ██║
    ██║  ██║██╔══██╗██║██╔══╝     ██║   ██║   ██║██║   ██║██╔══██║██╔══██╗██║  ██║
    ██████╔╝██║  ██║██║██║        ██║   ╚██████╔╝╚██████╔╝██║  ██║██║  ██║██████╔╝
    ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝        ╚═╝    ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝
EOF
echo "=========================================="
}

show_menu()
{
    echo "Select Resource Type:"
    echo "1. EC2 Drift Detection"
    echo "2. Security Group Drift Detection"
    echo "3. S3 Drift Detection"
    echo "4. Exit"
    echo
}
show_banner
show_menu


instance_type
ami
security_groups
iam_role
subnet
vpc
public_ip
ebs
tags
