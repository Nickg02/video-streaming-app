import cv2
import sqlite3

def capture():
    # define a video capture object
    # The argument 0 denotes that video is captured from default webcam
    cap = cv2.VideoCapture(0) 

    # Connect to an SQLite database
    conn = sqlite3.connect('video_frames.db')
    cursor = conn.cursor()

    # Create a table to store video frames
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS frames (
            frame_id INTEGER PRIMARY KEY,
            frame_data BLOB
        )
    ''')

    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to a binary format (e.g., JPEG)
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        # Store the binary frame data and frame_id in the database
        frame_data = buffer.tobytes()
        cursor.execute('INSERT INTO frames (frame_id, frame_data) VALUES (?, ?)', (frame_id, frame_data))
        frame_id += 1
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    # Commit the changes and close the database
    conn.commit()
    conn.close()
    
    # After the loop release the cap object 
    cap.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 