import React, { useState } from 'react';
import "../pagesCSS/SubmissionForm.css";

const SubmissionForm = () => {
  const [fileData, setFileData] = useState(null);
  const [popupMessage, setPopupMessage] = useState('');
  const [showPopup, setShowPopup] = useState(false);
  const [showWarning, setShowWarning] = useState(false);
  const [formData, setFormData] = useState({
    songTitle: '',
    artistName: '',
    songGenre: '',
    songDuration: '',
    songReleaseYear: '',
  });

  const showPopupMessage = (message) => {
    setPopupMessage(message);
    setShowPopup(true);
    setTimeout(() => setShowPopup(false), 1000); // Hide popup after 1 second
  };

  const isFormComplete = () => {
    return formData.songTitle && formData.artistName && formData.songGenre 
            && formData.songDuration && formData.songReleaseYear;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevState => ({
      ...prevState,
      [name]: value
    }));
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === "application/json") {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          if (Array.isArray(data) && data.every(song => isValidData(song))) {
            setFileData(data);
          } else {
            console.error('Invalid file format or file structure');
          }
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
      };
      reader.readAsText(file);
    } else {
      console.error('Please upload a valid JSON file');
    }
  };

  const isValidData = (song) => {
    const expectedFields = ['songTitle', 'artistName', 'songGenre', 'songDuration', 'songReleaseYear'];
    return expectedFields.every(field => field in song);
  };

  const submitData = async (data) => {
    try {
      const response = await fetch('http://127.0.0.1:8008/save_song_with_form', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (response.ok) {
        showPopupMessage('Song data submitted successfully');
        console.log('Song data submitted successfully');
        // Optionally, you can handle further UI updates here
      } else {
        showPopupMessage('Failed to submit song data');
        console.error('Failed to submit song data');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isFormComplete()) {
      setShowWarning(true);
      return;
    }
    setShowWarning(false);
    await submitData(formData);
  };

  const handleImportSubmit = async (e) => {
    e.preventDefault();
    if (fileData && fileData.length) {
      for (const song of fileData) {
        await submitData(song);
      }
    } else {
      console.error('No valid data to submit');
    }
  };

  return (
    <form className="submission-form">
      <h2>Add a song to the database</h2>
      <p>Please provide the details of the song you want to add</p>
      {/* Form Fields */}
      <input type="text" name="songTitle" value={formData.songTitle} onChange={handleChange} placeholder="Song Title" />
      <input type="text" name="artistName" value={formData.artistName} onChange={handleChange} placeholder="Artist's Name" />
      <input type="text" name="songGenre" value={formData.songGenre} onChange={handleChange} placeholder="Song's Genre" />
      <input type="text" name="songDuration" value={formData.songDuration} onChange={handleChange} placeholder="Song's Duration in seconds" />
      <input type="text" name="songReleaseYear" value={formData.songReleaseYear} onChange={handleChange} placeholder="Song's Release Year" />
      <button type="submit" onClick={handleSubmit} disabled={!isFormComplete()}>Submit</button>
      {showWarning && <div className="warning-popup">Please fill out all fields before submitting.</div>}
      {/* File Import */}
      <input type="file" accept=".json" onChange={handleFileChange} />
      <button onClick={handleImportSubmit}>Import</button>
      {showPopup && <div className="popup-message">{popupMessage}</div>}
    </form>
  );
};

export default SubmissionForm;
