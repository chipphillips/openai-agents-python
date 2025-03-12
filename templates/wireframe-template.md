# Wireframe Template

Here’s a structured, reusable **Wireframe Output Template** designed for AI agents to generate project-specific wireframes based on your requests. It includes formatting rules and placeholders for dynamic inputs:

---

## **AI Wireframe Output Template**  

*(For Project: {Project Name} – Page: {Page Name/Location})*  

### **1. Page Context**  

- **Page Type**: *[E.g., Landing Page, Dashboard, Contact Form]*  
- **Primary Goal**: *[1-sentence objective, e.g., "Convert visitors to newsletter signups"]*  
- **User Flow Stage**: *[Where does this page sit? E.g., "Post-login, step 3 of onboarding"]*  

#### **2. Core Components**  

```plaintext
[Component Type] [Placeholder Label] [Priority (1-5)]  
----------------------------------------  
Example:  
Header | [Global Nav] | Priority 1  
Hero Section | [Headline + CTA] | Priority 1  
Form | [Email Capture] | Priority 2  
Footer | [Social Links] | Priority 3  
```  

*(Replace with your components)*  

#### **3. Layout Structure**  

- **Grid**: `[Grid System, e.g., 12-column, 3-Zone Layout (Header/Main/Footer)]`  
- **Breakpoints**:  
  - Mobile (`<768px`): `[Stack columns, hide secondary CTAs]`  
  - Desktop (`>1024px`): `[Sidebar visible, 2-column grid]`  
- **Spacing**: `[Baseline: 8px | Padding: 16px]`  

#### **4. Annotations & Logic**  

```plaintext
[Element ID] [Note]  
-------------------  
Example:  
CTA_Button_1 | "Triggers email modal (see Modal_1)"  
Image_Carousel | "Auto-rotates every 5s (API-driven)"  
```  

#### **5. SEO & Accessibility**  

- **Key Headlines**: `[H1: {Primary Keyword}, H2: {Secondary Keyword}]`  
- **Alt Text Placeholders**: `[Image_1: "Descriptive alt text required"]`  
- **ARIA Labels**: `[Form_1: "Newsletter signup"]`  

#### **6. Tools Integration**  

- **v0 Instructions**:  

  ```plaintext
  Use component: [v0_button_primary] for CTAs  
  Data source: [API endpoint: /users/newsletter]  
  ```  

- **DeepSeek Prompt**:  
  `"Suggest a layout variation for {Component} emphasizing {Goal}"`  

#### **7. Export Format**  

- **Fidelity**: `[Low/Medium/High]`  
- **File Type**: `[Figma, PDF, v0 JSON, React Code]`  
- **Notes for Developers**: `[E.g., "Use mobile-first CSS"]`  

---

### **Formatting Rules for AI Agents**  

1. **Placeholders**:  
   - Use `{curly braces}` for dynamic inputs (e.g., `{Project Name}`).  
   - Media: `[Image: 16:9 ratio]`, `[Video: 60s max]`.  
2. **Annotations**:  
   - Label interactive elements with `[ID]` (e.g., `CTA_Button_1`).  
   - Use `|` separators for tabular data.  
3. **Avoid Markdown**: If exporting to code, use plaintext or v0’s syntax.  
4. **Responsive Hints**: Specify breakpoint logic (e.g., `hide_on_mobile`).  

---

### **Example Output**  

**Project**: *E-Commerce Site* | **Page**: *Product Listing Page*  

```plaintext
1. Page Context  
- Page Type: Product Grid  
- Primary Goal: "Drive clicks to product detail pages"  
- User Flow Stage: "Post-search results"  

2. Core Components  
Header | [Search Bar + Logo] | Priority 1  
Product Grid | [4-column, Image + Price] | Priority 1  
Filters | [Dropdown: Category, Price] | Priority 2  
Pagination | [1-5, Next/Prev] | Priority 3  

3. Layout Structure  
- Grid: 12-column (Desktop), 4-column (Mobile)  
- Breakpoints:  
  - Mobile: "Stack filters above grid"  
- Spacing: 24px between product cards  

4. Annotations  
Product_Image_1 | "Link to detail page (ID: PDP_1)"  
Price_Filter | "Updates grid via API: /products?price=low-high"  

5. Tools Integration  
- v0: Use `v0_product_card` component (props: image, title, price)  
- DeepSeek: "Suggest a better filter placement for mobile"  
```  

---

This template:  

- Standardizes AI output for consistency.  
- Works with v0/DeepSeek’s capabilities.  
- Includes technical specs for developers.  
- Allows easy scaling (add/remove sections).  

Let me know if you’d like to refine this further!
