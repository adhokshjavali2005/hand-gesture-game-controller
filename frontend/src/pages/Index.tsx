import Header from "@/components/Header";
import HeroSection from "@/components/HeroSection";
import FeaturesSection from "@/components/FeaturesSection";
import HowItWorksSection from "@/components/HowItWorksSection";
import GestureControlsSection from "@/components/GestureControlsSection";
import TechStackSection from "@/components/TechStackSection";
import SystemRequirementsSection from "@/components/SystemRequirementsSection";
import DownloadSection from "@/components/DownloadSection";
import Footer from "@/components/Footer";

const Index = () => (
  <>
    <Header />
    <main>
      <HeroSection />
      <FeaturesSection />
      <HowItWorksSection />
      <GestureControlsSection />
      <TechStackSection />
      <SystemRequirementsSection />
      <DownloadSection />
    </main>
    <Footer />
  </>
);

export default Index;
