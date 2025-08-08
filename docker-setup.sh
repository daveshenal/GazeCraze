#!/bin/bash

# Docker setup script for GazeCraze application

set -e

echo "Setting up GazeCraze Docker environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not available. Please ensure Docker Desktop is running."
    exit 1
fi

# Function to enable X11 forwarding for GUI applications
setup_x11() {
    echo "Setting up X11 forwarding for GUI display..."
    
    # Check if running on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS detected - X11 forwarding through Docker Desktop"
        echo "Note: Make sure Docker Desktop is running with GUI support enabled"
    else
        # Allow X11 forwarding (needed for OpenCV GUI on Linux)
        if command -v xhost &> /dev/null; then
            xhost +local:docker
        else
            echo "Warning: xhost not found. X11 forwarding may not work."
        fi
    fi
    
    # Export DISPLAY variable if not set
    if [ -z "$DISPLAY" ]; then
        export DISPLAY=:0
        echo "DISPLAY variable set to :0"
    fi
    
    echo "X11 setup complete."
}

# Function to check camera access
check_camera() {
    echo "Checking camera access..."
    
    # Check if running on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS detected - Camera access through Docker Desktop"
        echo "Note: Docker Desktop on macOS handles camera access automatically"
        echo "Make sure to allow camera access when prompted"
    else
        # Linux camera check
        if [ -e /dev/video0 ]; then
            echo "Camera device /dev/video0 found."
        else
            echo "Warning: No camera device found at /dev/video0"
            echo "You may need to:"
            echo "  1. Connect a camera"
            echo "  2. Check camera permissions"
            echo "  3. Adjust the device path in docker-compose.yml"
        fi
    fi
}

# Function to build the Docker image
build_image() {
    echo "Building GazeCraze Docker image..."
    docker compose build
    echo "Build complete."
}

# Function to run the application
run_app() {
    echo "Starting GazeCraze application..."
    echo "Press 'q' in the application window to quit"
    echo "Press 'r' in the application window to reset history"
    
    docker compose up gazecraze
}

# Function to run in development mode
run_dev() {
    echo "Starting GazeCraze in development mode..."
    echo "Source code will be mounted for live editing"
    
    docker compose --profile dev up gazecraze-dev
}

# Function to stop all containers
stop_containers() {
    echo "Stopping all GazeCraze containers..."
    docker compose down
}

# Function to clean up Docker resources
cleanup() {
    echo "Cleaning up Docker resources..."
    docker compose down --rmi local --volumes
    echo "Cleanup complete."
}

# Main menu
show_menu() {
    echo ""
    echo "GazeCraze Docker Setup"
    echo "====================="
    echo "1. Setup X11 and check camera"
    echo "2. Build Docker image"
    echo "3. Run application"
    echo "4. Run in development mode"
    echo "5. Stop containers"
    echo "6. Clean up Docker resources"
    echo "7. Full setup and run"
    echo "8. Exit"
    echo ""
}

# Full setup function
full_setup() {
    setup_x11
    check_camera
    build_image
    run_app
}

# Parse command line arguments
case "${1:-menu}" in
    "setup-x11")
        setup_x11
        ;;
    "check-camera")
        check_camera
        ;;
    "build")
        build_image
        ;;
    "run")
        run_app
        ;;
    "dev")
        run_dev
        ;;
    "stop")
        stop_containers
        ;;
    "cleanup")
        cleanup
        ;;
    "full")
        full_setup
        ;;
    "menu")
        while true; do
            show_menu
            read -p "Please choose an option (1-8): " choice
            
            case $choice in
                1) setup_x11; check_camera ;;
                2) build_image ;;
                3) run_app ;;
                4) run_dev ;;
                5) stop_containers ;;
                6) cleanup ;;
                7) full_setup ;;
                8) echo "Goodbye!"; exit 0 ;;
                *) echo "Invalid option. Please choose 1-8." ;;
            esac
            
            echo ""
            read -p "Press Enter to continue..."
        done
        ;;
    *)
        echo "Usage: $0 [setup-x11|check-camera|build|run|dev|stop|cleanup|full|menu]"
        echo ""
        echo "Commands:"
        echo "  setup-x11     - Setup X11 forwarding for GUI"
        echo "  check-camera  - Check camera device availability"
        echo "  build         - Build Docker image"
        echo "  run           - Run the application"
        echo "  dev           - Run in development mode"
        echo "  stop          - Stop all containers"
        echo "  cleanup       - Clean up Docker resources"
        echo "  full          - Full setup and run"
        echo "  menu          - Show interactive menu (default)"
        exit 1
        ;;
esac
