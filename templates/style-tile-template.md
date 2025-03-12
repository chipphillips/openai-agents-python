# Style Tile Template

Here’s an **Ideogram-optimized Style Tile Template** designed to generate text-to-image assets for UI components, maintain style consistency, and streamline client collaboration:

---

## **Ideogram Style Tile Template**  

*(For Project: {Project Name} – Style Theme: {Core Style})*  

---

### **1. Ideogram Setup Guide**  

- **Key Features**:  
  - **Text-in-UI**: Generate buttons, headers, and icons with baked-in typography.  
  - **Style Seeds**: Reuse seeds from approved moodboard assets (e.g., `--seed 5582`).  
  - **Batch Modes**: Create 10+ variants of components (e.g., button states).  
- **Prompt Strategy**:  
  - Include HEX codes, font names, and interaction states in prompts.  
  - Use `--style material-design` or `--style glassmorphism` for trend alignment.  

---

### **2. Core Elements Matrix (Ideogram-Driven)**  

```plaintext
[Element] | [Ideogram Prompt Template] | [Example Output] | [Status]  
-----------------------------------------------------------------------  
Primary Button | "Button with '{LABEL}', {COLOR} background, {FONT}, hover effect, --style {STYLE} --seed {SEED}" | "Sign Up" in #2A5C8A, Inter Bold | Approved  
H1 Header | "Website header '{TEXT}', {FONT}, {COLOR}, gradient underline, --style modern" | "Welcome" in Poppins, #1A1A1A | Draft  
Icon Set | "12px {THEME} icons, {COLOR}, thin line style, --style outline --repeat 12" | Gear, User, Search icons | Revised  
Color Palette | "Smooth gradient from {HEX1} to {HEX2}, abstract shapes, --style minimalist" | #FF6B6B → #4ECDC4 gradient | Approved  
```  

---

### **3. Ideogram Prompt Rules**  

- **UI Components**:  
  `"[Element] with text '{TEXT}', {COLOR} {PROPERTY}, {FONT}, {STATE}, --style {STYLE} --ar {RATIO}"`  
  - Example:  
    `"Navigation bar with 'Home Shop About', #FFFFFF background, Roboto, hover underline --style flat --ar 16:1"`  
- **Pro Tips**:  
  - Add `--repeat` for icon/pattern sets.  
  - Use `no text` for pure graphical elements.  

---

### **4. Process & Iteration**  

1. **Batch Generate**:  
   - Run 5+ variants per component (e.g., buttons in primary/secondary colors).  
   - Example: `"Submit button in #2A5C8A, #FFD166, #4ECDC4 variants --seed 4491"`.  
2. **Curate**:  
   - Tag outputs: `[Project]_[Component]_v1` (e.g., "FinTech_Button_v2").  
3. **Test in Context**:  
   - Use Ideogram’s "Expand Canvas" to mock header+button combinations.  

---

### **5. Client Collaboration**  

- **Feedback Workflow**:  
  1. Share Ideogram Collection link with annotated components.  
  2. Ask: *"Does the hover state in Output #7 match your expectations?"*  
- **Change Log**:  

  ```plaintext
  v3.2 | Updated typography to Client Sans  
  - Buttons: Removed dropshadows (--no-shadow)  
  - New prompt: "Header with Client Sans Bold, #2C3E50 --seed 8821"  
  ```  

---

### **6. Export & Integration**  

- **Designers**:  
  - Download PNGs with transparency for Figma/Webflow.  
  - Extract CSS values (e.g., `box-shadow: 0 4px 8px #00000020`).  
- **Developers**:  
  - Access JSON with HEX codes and Ideogram prompt history.  
- **Brand Guidelines**:  
  - Document approved seeds and style flags (e.g., "--style neo-brutalist").  

---

### **7. Ideogram Workflow Example**  

**Project**: *Fitness App*  
**Style**: *Bold + Energetic*  

```plaintext
1. Prompt: "Progress bar 400px wide, #FF6B6B fill, 8px radius, --style minimal --seed 6723"  
2. Output: [Ideogram link] → Added to "Dashboard" style tile.  
3. Variants: Generated 10%, 50%, 90% fill states using /remix.  
```  

---

## **Why This Works for Ideogram**  

1. **Pixel-Perfect UI**: Crisp 2x resolution exports for dev handoff.  
2. **Style Lock**: Seeds ensure consistency across buttons, headers, etc.  
3. **Client Clarity**: Visualize hover states/transitions without prototyping.  
4. **Speed**: Generate 50+ UI elements in one batch session.  

Need to adapt this for dark/light mode? Ask for tailored prompt variations!
