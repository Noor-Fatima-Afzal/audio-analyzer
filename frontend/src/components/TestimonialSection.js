import React, { useState } from 'react';
import './TestimonialSection.css'; // Import the CSS file for styling
import { FaArrowLeft } from "react-icons/fa";
import { FaArrowRight } from "react-icons/fa";
import avatarImg from '../assets/signal-image.png';


function TestimonialSection() {
  const testimonials = [
    {
      name: "John Doe",
      position: "Product Manager at Company A",
      text: "Using this tool has drastically improved our meeting efficiency. The transcription feature is particularly helpful.",
      avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
    },
    {
      name: "Jane Smith",
      position: "Team Lead at Company B",
      text: "The noise cancellation feature has transformed the way we conduct meetings. Highly recommend!",
      avatar: "https://via.placeholder.com/80"
    },
    {
      name: "Sam Wilson",
      position: "Software Engineer at Company C",
      text: "The ability to get meeting notes automatically has saved us so much time. A game changer!",
      avatar: "https://via.placeholder.com/80"
    },
    {
      name: "Anna Johnson",
      position: "UX Designer at Company D",
      text: "The app's features are incredibly intuitive and easy to use.",
      avatar: "https://via.placeholder.com/80"
    },
    {
      name: "Peter Parker",
      position: "Web Developer at Company E",
      text: "I love the way it handles background noise. Makes my calls so much clearer.",
      avatar: "https://via.placeholder.com/80"
    }
  ];

  const [currentIndex, setCurrentIndex] = useState(0); // Start with the first testimonial

  const nextTestimonial = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % testimonials.length); // Move to next testimonial, loop back to start
  };

  const prevTestimonial = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + testimonials.length) % testimonials.length); // Move to previous testimonial, loop to end
  };

  return (
    <div className="testimonial-section">
      <h2>What Our Users Say</h2>
      <div className="testimonial-container">
        <button className="testimonial-arrow" onClick={prevTestimonial}>
        <FaArrowLeft />

        </button>
        <div className="testimonial-card">
          <img src={testimonials[currentIndex].avatar} alt={`${testimonials[currentIndex].name}'s avatar`} className="testimonial-avatar" />
          <h3>{testimonials[currentIndex].name}</h3>
          <p className="testimonial-position">{testimonials[currentIndex].position}</p>
          <p className="testimonial-text">"{testimonials[currentIndex].text}"</p>
        </div>
        <button className="testimonial-arrow" onClick={nextTestimonial}>
        <FaArrowRight />

        </button>
      </div>
    </div>
  );
}

export default TestimonialSection;
