# Ideogram Moodboard Template

 Here’s your **Ideogram-Specific Moodboard Template**, optimized for seamless text-to-image generation, typography integration, and brand consistency. I’ve tailored prompts, workflows, and exports for Ideogram’s unique features (like text-in-image capabilities):

---

## **Ideogram Moodboard Template**  

*(For Project: {Project Name} – Theme: {Core Theme/Emotion})*  

---

### **1. Ideogram Setup Guide**  

- **Key Features to Leverage**:  
  - **Text-in-Image**: Perfect for logos, slogans, or typography experiments.  
  - **Style Consistency**: Use "Seed" values to replicate successful styles.  
  - **Aspect Ratios**: Optimize for social/media (e.g., `--ar 9:16` for Instagram Stories).  
- **Account Tips**:  
  - Save favorite outputs to "Collections" for client reviews.  
  - Use "Remix" to iterate on approved concepts.  

---

#### **2. Core Elements Matrix (Ideogram-Focused)**  

```plaintext
[Element Type] | [Ideogram Prompt Template] | [Example Output]  
-----------------------------------------------------------------------  
Typography | "3D neon text '{WORD}', {STYLE}, glowing {COLOR}, {MOOD}, 8K --ar 1:1 --style illustrative" | "HOPE" in pink neon, retro vaporwave  
Pattern | "Seamless {MATERIAL} pattern with hidden text '{PHRASE}', {COLORS}, --tile" | Geometric linen texture with "Breathe" in subtle emboss  
Logo Concept | "Minimalist {INDUSTRY} logo, {ANIMAL} icon, text '{BRAND NAME}', {COLOR} --style flat" | Fox icon + "Forestry" in sage green  
Photography | "Cinematic {SCENE}, text overlay '{QUOTE}', {LIGHTING}, {MOOD} --style hyperreal" | Sunset beach with "Wander Further" in script  
```  

---

#### **3. Ideogram Prompt Design Rules**  

- **Text-in-Image Formula**:  
  `"Text '{TEXT}' in {FONT_STYLE}, {CONTEXT}, {COLOR_PALETTE}, {MOOD} --style {STYLE} --ar {RATIO}"`  
  - Example:  
    `"Text 'Explore' in bold serif, mountain backdrop, teal/gold, adventurous --style vintage poster --ar 3:2"`  
- **Pro Tips**:  
  - Use **quotes** around text (`"Hello"`) for clarity.  
  - Add `--style illustrative` for hand-drawn text.  
  - For subtle text: Add keywords like "faded," "embossed," or "watermark."  

---

#### **4. Process & Iteration**  

1. **Batch Generation**:  
   - Run 4-6 variations per prompt using Ideogram’s "Generate Similar."  
   - Example: Test "Retro diner sign" vs. "Cyberpunk neon sign" for a 1950s brand.  
2. **Curate**:  
   - Filter by Ideogram’s "Vibrant," "Natural," or "Muted" tags to match mood.  
3. **Refine**:  
   - Use "Seed" numbers from top outputs (e.g., `--seed 5832`) for consistency.  

---

#### **5. Feedback & Collaboration**  

- **Client Reviews**:  
  - Share Ideogram Collection links for live commenting.  
  - Ask: *"Does the text style in Output #3 match your brand voice?"*  
- **Version Log**:  

  ```plaintext
  v2.1 | Added "Adventure" logo concepts (Seed 4451 + 8923)  
  - Client feedback: "More contrast between text and background."  
  - Next step: Remix with `--contrast 1.2`  
  ```  

---

#### **6. Export & Integration**  

- **Designers**:  
  - Download PNGs with transparent backgrounds (Ideogram Pro feature).  
  - Extract HEX codes from text/graphics using Figma’s color picker.  
- **Developers**:  
  - Use Ideogram’s text-in-image outputs as placeholder graphics.  
- **Brand Guidelines**:  
  - Document successful prompts (e.g., "Primary font: bold sans-serif + `--style modern`").  

---

#### **7. Ideogram Workflow Example**  

**Project**: *Coffee Shop Branding*  
**Goal**: *Rustic + Modern*  

```plaintext
1. Prompt: "Handwritten chalkboard text 'Daily Brew', coffee beans background, warm browns, cozy --style realistic --ar 4:3"  
2. Output: [Ideogram link] → Approved for menu design.  
3. Seed: 7782 → Used for all signage concepts.  
```  

---

### **Why This Works for Ideogram**  

1. **Text Precision**: Leverages Ideogram’s best-in-class text rendering.  
2. **Style Control**: Uses `--style` and `--seed` for predictable iterations.  
3. **Client Alignment**: Shared collections simplify feedback loops.  
4. **Handoff Efficiency**: Transparent PNGs integrate directly into Figma/Webflow.  

Need help crafting a specific prompt (e.g., combining textures + text)? Just ask!
