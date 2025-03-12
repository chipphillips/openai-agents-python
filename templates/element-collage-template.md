# Element Collage Template

Here’s an **Ideogram-Optimized Element Collage Template** tailored for generating interactive UI components, animations, and state variations using text-to-image AI. It includes structured prompts, device-specific rules, and seamless handoff workflows:

---

## **Ideogram Element Collage Template**  

*(For Project: {Project Name} – Component Type: {Core Interaction})*  

---

### **1. Ideogram Setup Guide**  

- **Key Features**:  
  - **State Variations**: Generate hover/active/focus states using `--state` parameter (e.g., `--state hover`).  
  - **Device Mockups**: Use `--ar 9:16` for mobile, `--ar 16:9` for desktop.  
  - **Animation Hints**: Add `--motion blur` or `--transition slide` for motion cues.  
- **Prompt Strategy**:  
  - Include interaction descriptors (e.g., "pressed", "loading", "error").  
  - Reference approved style tile seeds (e.g., `--seed 5582` from buttons).  

---

### **2. Core Elements Matrix (Ideogram-Driven)**  

```plaintext
[Component] | [Ideogram Prompt Template] | [Example Output] | [States]  
-----------------------------------------------------------------------  
Dropdown Menu | "Navigation dropdown, {COLOR}, {FONT}, hover highlight, --state {STATE} --seed 4491" | #2A5C8A bg, Inter | Default/Hover/Open  
Form Input | "Text field '{PLACEHOLDER}', {COLOR} border, error state, --style material --state error" | "Enter email" with red alert | Active/Error/Success  
Image Carousel | "3-card carousel, {COLOR} pagination, hover zoom, --ar 16:9 --motion blur" | Teal dots, +10% scale on hover | Static/Hover  
Mobile Menu | "Hamburger > expanded menu, {BREAKPOINT}, {COLOR}, --ar 9:16" | #1A1A1A overlay, 768px | Collapsed/Open  
```  

---

### **3. Ideogram Prompt Rules**  

- **Interactive States**:  
  `"[Component] in {STATE}, {STYLE}, {INTERACTION}, {FEEDBACK} --state {STATE} --seed {SEED}"`  
  - Example:  
    `"Checkbox checked, #4ECDC4 fill, bounce animation --state active --seed 7782"`  
- **Pro Tips**:  
  - Use `--no-text` for non-labeled elements (e.g., loading spinners).  
  - Add `--sequence 3` for multi-step animations.  

---

### **4. Process & Iteration**  

1. **Batch Generate States**:  
   - Run parallel prompts for `--state default`, `--state hover`, `--state active`.  
   - Example: `"Button '{LABEL}' in 3 states --variation 3 --seed 4491"`.  
2. **Curate Interactions**:  
   - Tag files: `[Project]_[Component]_[State]_v[#]` (e.g., "SaaS_DeleteBtn_Hover_v2").  
3. **Test Responsiveness**:  
   - Use Ideogram’s "Expand Canvas" to show mobile/desktop transitions.  

---

### **5. Collaboration & Workflow**  

- **Developer Notes**:  

  ```plaintext
  Checkbox_Checked:  
  - HEX: #4ECDC4  
  - Motion: 200ms bounce (refer to Ideogram output #449)  
  - Prompt: "Checkbox checked state, spring animation --seed 6723"  
  ```  

- **Feedback System**:  
  - Share Ideogram collection links with `?annotation=1` for inline comments.  
  - Version log:  

    ```plaintext  
    v2.3 | Added loading spinners  
    - Prompt: "Loading spinner, #2A5C8A, 8-dot cycle --style minimal"  
    - States: Default/Loading/Complete  
    ```  

---

### **6. Export & Integration**  

- **Designers**:  
  - Download PNG sequences for Figma prototypes (e.g., hover_001 → hover_003).  
  - Extract CSS animations: `@keyframes` values from motion prompts.  
- **Developers**:  
  - Access JSON with state metadata:  

    ```json  
    {  
      "button_primary": {  
        "default": "prompt: 'Button #2A5C8A, rest state --seed 5582'",  
        "hover": "prompt: 'Add 10% brightness --seed 5582 --remix'"  
      }  
    }  
    ```  

---

### **7. Ideogram Workflow Example**  

**Project**: *E-Learning Platform*  
**Component**: *Video Player Controls*  

```plaintext  
1. Prompt: "Video play button, #FF6B6B, hover scale 110% --state hover --seed 8821"  
2. Output: [Ideogram link] → Approved for all media players.  
3. States: Generated paused/playing/loading via /remix.  
```  

---

## **Why This Works for Ideogram**  

1. **Interaction-First**: Visualize states without coding.  
2. **Style Consistency**: Seeds lock colors/typography across components.  
3. **Motion Hints**: `--motion` flags guide animation development.  
4. **Responsive Ready**: Aspect ratios map to breakpoints.  

Need to create complex component systems (e.g., data tables with sorting)? Ask for advanced prompt structures!
