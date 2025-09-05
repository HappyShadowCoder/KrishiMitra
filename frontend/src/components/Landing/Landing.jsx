import { useEffect, useState } from "react";
import Nav from "../Nav";
import Hero from "../Hero";
import Features from "../Features";
import Contact from "../Contact";
import About from "../About";

export default function Landing() {
  const [aboutData, setAboutData] = useState(null);
  const [featuresData, setFeaturesData] = useState(null);
  const [contactData, setContactData] = useState(null);

  useEffect(() => {
    // Replace URLs with your actual backend endpoints
    fetch("/api/about")
      .then((res) => res.json())
      .then((data) => setAboutData(data))
      .catch(() => setAboutData(null));

    fetch("/api/features")
      .then((res) => res.json())
      .then((data) => setFeaturesData(data))
      .catch(() => setFeaturesData(null));

    fetch("/api/contact")
      .then((res) => res.json())
      .then((data) => setContactData(data))
      .catch(() => setContactData(null));
  }, []);

  return (
    <>
      <div className="absolute top-0 left-0 w-full bg-white overflow-x-hidden">
        <Nav />
        <Hero />
        <About data={aboutData} />
        <Features data={featuresData} />
        <Contact data={contactData} />
      </div>
    </>
  );
}
