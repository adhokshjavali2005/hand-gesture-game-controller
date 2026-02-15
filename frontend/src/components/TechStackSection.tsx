import { motion } from "framer-motion";

const techs = [
  { name: "Python", desc: "Core application logic" },
  { name: "OpenCV", desc: "Video capture & processing" },
  { name: "MediaPipe", desc: "Hand landmark detection" },
  { name: "NumPy", desc: "Data computation" },
  { name: "PyAutoGUI", desc: "Keyboard simulation" },
];

const TechStackSection = () => (
  <section id="tech-stack" className="py-24 md:py-32 bg-secondary/30">
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
          Built <span className="text-primary">With</span>
        </h2>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Powered by industry-leading open-source technologies.
        </p>
      </motion.div>

      <div className="flex flex-wrap justify-center gap-4 max-w-3xl mx-auto">
        {techs.map((t, i) => (
          <motion.div
            key={t.name}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="flex items-center gap-3 rounded-full bg-card border border-border px-6 py-3 hover:border-primary/40 transition-colors"
          >
            <span className="w-2 h-2 rounded-full bg-primary animate-pulse-glow" />
            <div>
              <span className="font-display text-sm font-semibold">{t.name}</span>
              <span className="text-xs text-muted-foreground ml-2">{t.desc}</span>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default TechStackSection;
