import { motion } from "framer-motion";
import { Eye, Cpu, Sun, Zap, Gamepad2 } from "lucide-react";

const features = [
  { icon: Eye, title: "Real-Time Hand Tracking", desc: "Powered by MediaPipe for accurate, instant hand detection." },
  { icon: Cpu, title: "21-Point Landmark Detection", desc: "Precise tracking of every joint and fingertip on your hand." },
  { icon: Sun, title: "Works in Any Lighting", desc: "Robust detection that adapts to various lighting conditions." },
  { icon: Zap, title: "30+ FPS, Low Latency", desc: "Smooth and responsive gameplay with minimal input delay." },
  { icon: Gamepad2, title: "Arrow Key Compatible", desc: "Works with any game that uses arrow key controls." },
];

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.5 },
  }),
};

const FeaturesSection = () => (
  <section id="features" className="py-24 md:py-32">
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
          Powerful <span className="text-primary">Features</span>
        </h2>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Built with cutting-edge computer vision technology for the best gaming experience.
        </p>
      </motion.div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6 max-w-5xl mx-auto">
        {features.map((f, i) => (
          <motion.div
            key={f.title}
            custom={i}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            variants={cardVariants}
            className="group rounded-xl bg-card border border-border p-6 hover:border-primary/40 transition-all duration-300 gradient-border"
          >
            <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center mb-4 group-hover:bg-primary/20 transition-colors">
              <f.icon className="w-6 h-6 text-primary" />
            </div>
            <h3 className="font-display text-lg font-semibold mb-2">{f.title}</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default FeaturesSection;
