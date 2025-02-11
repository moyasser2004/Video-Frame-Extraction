import cv2
import os


class VideoProcessor:
    def __init__(self, video_path, output_folder):
        self.video_path = video_path
        self.output_folder = output_folder
        
        # Create the output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def extract_frames(self, sampling_interval=0.25):
        """
        Extract frames from a video and sample frames at regular intervals.
        
        :param sampling_interval: Fraction of video duration for sampling frames (default: 0.25 for quarters).
        :return: List of web-friendly paths to the sampled frames.
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            print(f"Error: Unable to open video file {self.video_path}")
            return []
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps

        sampled_frames = []
        num_samples = int(1 / sampling_interval)  # Number of samples based on interval
        
        for i in range(num_samples):
            target_time = (i + 0.5) * (duration * sampling_interval)
            cap.set(cv2.CAP_PROP_POS_MSEC, target_time * 1000)
            ret, frame = cap.read()
            
            if ret:
                frame_filename = f"frame_{i+1}.jpg"
                frame_path = os.path.join(self.output_folder, frame_filename)
                
                cv2.imwrite(frame_path, frame)
                
                # Convert file path to a URL-friendly format for web servers
                web_path = frame_path.replace('\\', '/')
                sampled_frames.append(web_path)
                
                print(f"Saved frame at: {web_path}")
            else:
                print(f"Warning: Unable to read frame at {target_time} seconds.")
        
        cap.release()
        return sampled_frames
