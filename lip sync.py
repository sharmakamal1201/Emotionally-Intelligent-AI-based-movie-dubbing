import os
import subprocess
from pathlib import Path

def mute_original_audio(input_video_path, output_muted_video_path):
    """
    Mute the original audio in the video.
    
    Args:
        input_video_path (str): Path to the input video file.
        output_muted_video_path (str): Path to save the muted output video.
    """
    subprocess.run([
        'ffmpeg', '-i', input_video_path, '-c', 'copy', '-an', output_muted_video_path
    ], check=True)
    print(f"Muted video saved at: {output_muted_video_path}")

def lip_sync_video(input_video_path, input_audio_path, output_path, wav2lip_model_path):
    """
    Perform lip syncing using the Wav2Lip model.
    
    Args:
        input_video_path (str): Path to the input video file.
        input_audio_path (str): Path to the new audio file.
        output_path (str): Path to save the lip-synced output video.
        wav2lip_model_path (str): Path to the pretrained Wav2Lip model.
    """
    command = [
        'python', 'Wav2Lip/inference.py', 
        '--checkpoint_path', wav2lip_model_path, 
        '--face', input_video_path, 
        '--audio', input_audio_path, 
        '--outfile', output_path
    ]
    
    subprocess.run(command, check=True)
    print(f"Lip-synced video saved at: {output_path}")

def replace_audio(input_video_path, input_audio_path, output_video_path):
    """
    Replace the original audio in a video with new audio.
    
    Args:
        input_video_path (str): Path to the input muted video file.
        input_audio_path (str): Path to the new audio file.
        output_video_path (str): Path to save the final video with replaced audio.
    """
    subprocess.run([
        'ffmpeg', '-i', input_video_path, '-i', input_audio_path, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_video_path
    ], check=True)
    print(f"Final video with replaced audio saved at: {output_video_path}")

if __name__ == "__main__":
    # File paths
    input_video_path = "input_video.mp4"  # Path to your original Hindi video
    input_audio_path = "dubbed_audio.wav"  # Path to your English dubbed audio
    output_muted_video_path = "muted_video.mp4"
    wav2lip_model_path = "wav2lip.pth"
    lip_synced_video_path = "lip_synced_video.mp4"
    final_output_path = "final_output_video.mp4"

    # Step 1: Mute the original audio
    mute_original_audio(input_video_path, output_muted_video_path)

    # Step 2: Perform lip syncing using Wav2Lip
    lip_sync_video(output_muted_video_path, input_audio_path, lip_synced_video_path, wav2lip_model_path)

    # Step 3: Replace the muted video audio with the dubbed English audio
    replace_audio(lip_synced_video_path, input_audio_path, final_output_path)
