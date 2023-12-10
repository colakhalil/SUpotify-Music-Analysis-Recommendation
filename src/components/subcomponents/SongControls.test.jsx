import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import SongControls from './SongControls'; // Adjust the import path as necessary

describe('SongControls Component', () => {
  // Test for checking if the play/pause button works
  it('toggles between play and pause', () => {
    const mockTogglePlay = jest.fn();
    const { rerender } = render(
      <SongControls
        isPlaying={false}
        togglePlay={mockTogglePlay}
        currentTime={0}
        songDurationInSeconds={180}
        song={{ duration: '03:00' }}
        toggleLyrics={() => {}}
        userRating={0}
        handleRatingChange={() => {}}
      />
    );

    // Check if the button shows "Play" initially
    const playButton = screen.getByText('Play');
    fireEvent.click(playButton);
    expect(mockTogglePlay).toHaveBeenCalled();

    // Rerender with isPlaying true and check if the button shows "Pause"
    rerender(
      <SongControls
        isPlaying={true}
        togglePlay={mockTogglePlay}
        currentTime={0}
        songDurationInSeconds={180}
        song={{ duration: '03:00' }}
        toggleLyrics={() => {}}
        userRating={0}
        handleRatingChange={() => {}}
      />
    );
    expect(screen.getByText('Pause')).toBeInTheDocument();
  });

  // Test for lyrics button
  it('calls toggleLyrics on lyrics button click', () => {
    const mockToggleLyrics = jest.fn();
    render(
      <SongControls
        isPlaying={false}
        togglePlay={() => {}}
        currentTime={0}
        songDurationInSeconds={180}
        song={{ duration: '03:00' }}
        toggleLyrics={mockToggleLyrics}
        userRating={0}
        handleRatingChange={() => {}}
      />
    );

    const lyricsButton = screen.getByText('Lyrics');
    fireEvent.click(lyricsButton);
    expect(mockToggleLyrics).toHaveBeenCalled();
  });

  // Test for song timer display
  it('displays the correct current time and song duration', () => {
    render(
      <SongControls
        isPlaying={false}
        togglePlay={() => {}}
        currentTime={120} // 2 minutes
        songDurationInSeconds={180}
        song={{ duration: '03:00' }}
        toggleLyrics={() => {}}
        userRating={0}
        handleRatingChange={() => {}}
      />
    );

    expect(screen.getByText('2:00 / 03:00')).toBeInTheDocument();
  });

  // Add more tests here if needed
});
