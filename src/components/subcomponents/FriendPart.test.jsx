import React from "react";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/extend-expect";
import FriendPart from "./FriendPart"; // Adjust the import path as necessary

describe("FriendPart Component", () => {
  const mockFriendData = {
    name: "John Doe",
    profilePicture: "https://example.com/profile.jpg",
    favoriteGenre: "Rock",
    bio: "Loves music and traveling",
  };

  it("renders the friend's information correctly", () => {
    render(<FriendPart friendData={mockFriendData} />);

    // Check if the name is rendered
    expect(screen.getByText("John Doe")).toBeInTheDocument();

    // Check if the image is rendered with the correct src and alt attributes
    const image = screen.getByRole('img', { name: "John Doe's profile" });
    expect(image).toHaveAttribute("src", "https://example.com/profile.jpg");
    expect(image).toHaveAttribute("alt", "John Doe's profile");

    // Check if the favorite genre is rendered
    expect(screen.getByText("Favorite Genre: Rock")).toBeInTheDocument();

    // Check if the bio is rendered
    expect(screen.getByText("Loves music and traveling")).toBeInTheDocument();
  });

  // Additional tests can be added to cover other scenarios
});
