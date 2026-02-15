import { motion } from "framer-motion";
import { ChevronDown } from "lucide-react";
import heroBg from "@/assets/hero-bg.jpg";

const HeroSection = () => (
  <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-16">
    {/* Background image */}
    <div className="absolute inset-0">
      <img src={heroBg} alt="" className="w-full h-full object-cover opacity-40" />
      <div className="absolute inset-0 bg-gradient-to-b from-background/60 via-background/80 to-background" />
    </div>

    <div className="relative z-10 container mx-auto px-4 text-center">
      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-primary font-display text-sm tracking-[0.3em] uppercase mb-4"
      >
        Hand Gesture Game Controller
      </motion.p>

      <motion.h1
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.1 }}
        className="font-display text-4xl sm:text-5xl md:text-7xl font-black leading-tight mb-6 text-glow"
      >
        Control Games with
        <br />
        <span className="text-primary">Hand Gestures</span>
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.25 }}
        className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-10"
      >
        Play Hill Climb Racing and other games with just your hand!
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="flex flex-col sm:flex-row gap-4 justify-center"
      >
        <a
          href="#download"
          className="inline-flex h-12 px-8 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold text-base hover:bg-primary/90 transition-all box-glow"
        >
          Download Now
        </a>
        <a
          href="#features"
          className="inline-flex h-12 px-8 items-center justify-center rounded-lg border border-border text-foreground font-semibold text-base hover:bg-secondary transition-all"
        >
          Learn More
        </a>
      </motion.div>
    </div>

    <motion.a
      href="#features"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 1 }}
      className="absolute bottom-8 left-1/2 -translate-x-1/2 text-muted-foreground hover:text-primary transition-colors animate-float"
    >
      <ChevronDown size={32} />
    </motion.a>
  </section>
);

export default HeroSection;
