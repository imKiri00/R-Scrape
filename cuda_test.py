import torch

def cuda_test():
    # Check if CUDA is available
    cuda_available = torch.cuda.is_available()
    print(f"CUDA available: {cuda_available}")

    if cuda_available:
        # Get the number of CUDA devices
        device_count = torch.cuda.device_count()
        print(f"Number of CUDA devices: {device_count}")

        # Print information for each device
        for i in range(device_count):
            device = torch.cuda.get_device_properties(i)
            print(f"\nDevice {i}:")
            print(f"  Name: {device.name}")
            print(f"  Total memory: {device.total_memory / 1e9:.2f} GB")

        # Create a sample tensor and move it to GPU
        x = torch.rand(1000, 1000)
        x_gpu = x.cuda()
        print("\nTensor successfully moved to GPU")

    else:
        print("CUDA is not available on this system.")

if __name__ == "__main__":
    cuda_test()