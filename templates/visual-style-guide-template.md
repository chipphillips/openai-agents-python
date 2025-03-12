# Visual Style Guide Template

Here’s an **Ideogram-Optimized Visual Style Guide Template** designed to generate and enforce brand consistency using text-to-image AI, dynamic component libraries, and collaborative workflows:

---

## **Ideogram Visual Style Guide Template**  

*(For Project: {Project Name} – Version: {Version Number})*  

---

### **1. Ideogram Integration Guide**  

- **Key Features**:  
  - **Asset Generation**: Create logos, icons, and UI components directly in Ideogram.  
  - **Style Lock**: Use `--seed` values from approved designs to ensure consistency.  
  - **AI-Powered Variations**: Batch-generate dark/light modes, seasonal themes, etc.  
- **Prompt Strategy**:  
  - Include HEX codes, font names, and interaction states in prompts.  
  - Use `--style` flags aligned with moodboard themes (e.g., `--style cyberpunk`).  

---

### **2. Core Sections & Ideogram Prompts**  

```plaintext
[Section] | [Ideogram Prompt Template] | [Example Output] | [Status]  
------------------------------------------------------------------------  
Brand Mark | "Logo '{BRAND NAME}', {INDUSTRY} icon, {COLOR}, {STYLE} --seed 4491" | TechCo + circuit icon | Locked  
Color System | "Gradient from {HEX1} to {HEX2}, abstract {THEME}, --palette" | #2A5C8A → #4ECDC4 w/ waves | Approved  
Button States | "Button '{LABEL}', {COLOR}, {FONT}, {STATE} --seed 5582" | "Submit" in 3 states | Iterating  
Data Viz | "Chart {TYPE}, {COLOR}, {STYLE}, --style data-ink" | Bar chart, #FF6B6B | Draft  
```  

---

### **3. AI-Powered Style Rules**  

- **Typography**:  

  ```plaintext
  H1: "Headline '{SAMPLE}', {FONT}, {COLOR}, --style modern --seed 8821"  
  Body: "Paragraph lorem ipsum, {FONT}, #1A1A1A, line-height 1.6 --no-effects"  
  ```  

- **Component Library**:  

  ```plaintext
  Primary Button: "Cta button '{TEXT}', #2A5C8A, Inter Bold, hover:scale(1.05) --seed 5582"  
  Form Error: "Alert message '{TEXT}', #FF6B6B border, fade-in --state error"  
  ```  

---

### **4. Process & Governance**  

1. **Batch Generation**:  
   - Run `--variation 5` on core components for team voting.  
   - Example: `"Generate 5 newsletter signup forms using --seed 6723"`.  
2. **Version Control**:  

   ```plaintext  
   v2.1.3 | 2024-03-20  
   - Added error states (Prompt: "Form error #FF6B6B, shake animation --seed 4491")  
   - Retired legacy button style (Seed 1122 deprecated)  
   ```  

3. **Accessibility Checks**:  
   - Use Ideogram’s contrast checker: `"Verify #2A5C8A/#FFFFFF contrast --wcag"`.  

---

### **5. Collaboration Workflow**  

- **Designer Handoff**:  
  - Figma plugin: Auto-import Ideogram assets via `@ideogram/figma-sync`.  
  - CSS export: `"Export button #2A5C8A as CSS variables --code"`.  
- **Developer Notes**:  

  ```json  
  {  
    "primary_button": {  
      "default": "prompt: 'Button #2A5C8A --seed 5582'",  
      "hover": "brightness(1.1) + scale(1.02)",  
      "motion": "200ms ease-in-out"  
    }  
  }  
  ```  

---

### **6. Living Document Features**  

- **AI Audit Trail**:  

  ```plaintext  
  2024-03-20: Generated dark mode variants via  
  "Dark theme toggle, #1A1A1A bg, --seed 4491 --remix"  
  ```  

- **Feedback Integration**:  

  ```plaintext  
  Client Request: "Softer error colors"  
  Action: Ran "Error state #FFB5B5, pulse animation --seed 4491-2"  
  ```  

---

### **7. Ideogram Workflow Example**  

**Project**: *AI Health Platform*  
**Update**: *Dark Mode Expansion*  

```plaintext  
1. Prompt: "Dark theme header, #1A1A1A, Inter SemiBold --seed 8821 --remix"  
2. Output: [Ideogram link] → Auto-synced to Figma  
3. CSS Update:  
   --color-header: #1A1A1A;  
   --font-header: Inter-SemiBold;  
```  

---

## **Export & Compliance**  

- **PDF Report**: Auto-generate with Ideogram’s `--export pdf` flag.  
- **WCAG Compliance**:  

  ```plaintext  
  Contrast Check: #2A5C8A/#FFFFFF → 4.8:1 (AA Pass)  
  Prompt: "Verify contrast for primary button --wcag"  
  ```  

- **Asset Library**:  
  - PNG/SVG: `ideogram export --format svg --component buttons`  
  - React: `ideogram export --code react --seed 5582`  

---

## **Why This Works with Ideogram**  

1. **Consistency at Scale**: Seeds enforce brand rules across teams.  
2. **Self-Documenting**: Prompts become style guide entries.  
3. **Dynamic Updates**: Remix entire sections with `--seed` + `--remix`.  
4. **Accessibility First**: Built-in contrast checks and alt text generation.  

Need to add multilingual support or complex components? Let’s refine the prompt library!
