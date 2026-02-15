import { motion } from "framer-motion";
import { Monitor, Camera, Cpu } from "lucide-react";

const requirements = [
  { icon: Monitor, title: "Operating System", items: ["Windows 10/11", "macOS 12+", "Linux (Ubuntu 20.04+)"] },
  { icon: Camera, title: "Webcam", items: ["720p or higher", "Built-in or external USB", "Stable mount recommended"] },
  { icon: Cpu, title: "Hardware", items: ["4 GB RAM minimum", "Any modern processor", "No GPU required"] },
];

const SystemRequirementsSection = () => (
  <section className="py-24 md:py-32">
    <div className="container mx-auto px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="text-center mb-16"
      >
        <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
          System <span className="text-primary">Requirements</span>
        </h2>
      </motion.div>

      <div className="grid sm:grid-cols-3 gap-6 max-w-4xl mx-auto">
        {requirements.map((r, i) => (
          <motion.div
            key={r.title}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            className="rounded-xl bg-card border border-border p-6"
          >
            <r.icon className="w-8 h-8 text-primary mb-4" />
            <h3 className="font-display text-base font-semibold mb-3">{r.title}</h3>
            <ul className="space-y-2">
              {r.items.map((item) => (
                <li key={item} className="text-sm text-muted-foreground flex items-start gap-2">
                  <span className="w-1 h-1 rounded-full bg-primary mt-2 shrink-0" />
                  {item}
                </li>
              ))}
            </ul>
          </motion.div>
        ))}
      </div>
    </div>
  </section>
);

export default SystemRequirementsSection;
