import pkg_resources

# List of required packages from your requirements file
required_packages = [
    "mediapipe",
    "opencv-python",
    "numpy",
]

# Find installed versions
output_lines = []
for pkg in required_packages:
    try:
        version = pkg_resources.get_distribution(pkg).version
        output_lines.append(f"{pkg}=={version}")
    except pkg_resources.DistributionNotFound:
        output_lines.append(f"# {pkg} not installed")

# Print the results
print("\n".join(output_lines))

# Optionally write to requirements.txt
with open("requirements.txt", "w") as f:
    f.write("\n".join(output_lines))

print("\nPinned versions saved to requirements.lock.txt")