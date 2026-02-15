import { motion } from "framer-motion";
import { Download, Github, Code } from "lucide-react";

const DownloadSection = () => (
  <section id="download" className="py-24 md:py-32 bg-secondary/30">
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center max-w-2xl mx-auto"
      >
        <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
          Ready to <span className="text-primary">Play?</span>
        </h2>
        <p className="text-muted-foreground mb-10">
          Download the application and start controlling games with your hands today.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href="https://github.com/adhokshjavali2005/hand-gesture-game-controller/releases/latest"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex h-14 px-8 items-center justify-center gap-3 rounded-xl bg-primary text-primary-foreground font-bold text-base hover:bg-primary/90 transition-all box-glow"
          >
            <Download className="w-5 h-5" />
            Download Executable
          </a>
          <a
            href="https://github.com/adhokshjavali2005/hand-gesture-game-controller"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex h-14 px-8 items-center justify-center gap-3 rounded-xl border border-border text-foreground font-semibold text-base hover:bg-secondary transition-all"
          >
            <Github className="w-5 h-5" />
            GitHub Repo
          </a>
          <a
            href="https://github.com/adhokshjavali2005/hand-gesture-game-controller/archive/refs/heads/main.zip"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex h-14 px-8 items-center justify-center gap-3 rounded-xl border border-border text-foreground font-semibold text-base hover:bg-secondary transition-all"
          >
            <Code className="w-5 h-5" />
            Source Code
          </a>
        </div>
      </motion.div>
    </div>
  </section>
);

export default DownloadSection;
