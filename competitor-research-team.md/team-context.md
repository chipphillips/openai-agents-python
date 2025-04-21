# LLM-Optimized Prompts for Construction Tech Competitive Analysis

I've created a comprehensive set of prompts designed to help you analyze your competitive intelligence reports in a logical sequence. These prompts will help you extract maximum value from your CB Insights reports and generate professional-grade strategic analysis.

## Part 1: LLM-Optimized Prompts for Analysis

### Initial Data Extraction Prompts

1. **Basic Company Profile Extraction**
```
Analyze this CB Insights report on [COMPANY NAME] and extract the following information in a structured format: company name, founding date, headquarters location, funding status (total raised and latest round), valuation (if available), and brief business description. Present this as a concise company profile suitable for a competitive intelligence database.
```

2. **Product and Service Offering Analysis**
```
Review this CB Insights report on [COMPANY NAME] and provide a detailed analysis of their product/service offerings. Include: primary solutions, key features, target construction processes they're addressing, pricing model (if mentioned), and how they position themselves in the market. Analyze how their offerings address specific pain points in the construction industry.
```

3. **Funding and Investor Analysis**
```
From this CB Insights report on [COMPANY NAME], analyze their funding history in detail. Include: total funding raised, number of funding rounds, dates and amounts of each round, lead investors, other notable investors, and what this funding trajectory suggests about their growth strategy and market validation. Compare this to typical funding patterns in construction tech.
```

4. **Leadership Team Assessment**
```
Based on the CB Insights report for [COMPANY NAME], analyze their leadership team. Include: key executives, their backgrounds and previous experience, expertise they bring to the company, and any patterns or strengths in the team composition. Assess how their leadership expertise might influence the company's strategic direction and competitive advantage.
```

### Competitive Landscape Analysis Prompts

5. **Direct Competitor Identification**
```
Analyze this CB Insights report and identify [COMPANY NAME]'s direct competitors. For each competitor, extract: company name, funding amount, primary product focus, target customer segment, and key differentiators. Then provide a strategic assessment of how these companies directly compete with each other and with Constructiv AI's planned offerings.
```

6. **Market Positioning Analysis**
```
Based on this CB Insights report, analyze [COMPANY NAME]'s market positioning. Include: their primary value proposition, target customer segments, pricing strategy (if available), key messaging themes, and how they differentiate from competitors. Then evaluate the strength of their positioning and identify any gaps or weaknesses that could be exploited by a new market entrant.
```

7. **Technology Stack and Innovation Assessment**
```
From the CB Insights report on [COMPANY NAME], analyze their technology approach and innovation strategy. Include: core technologies used (AI, machine learning, etc.), unique technical capabilities, patent information (if available), and recent product innovations. Assess how their technology creates competitive advantages and any potential barriers to entry they've established.
```

### Strategic Analysis Prompts

8. **Market Entry Strategy Analysis**
```
Review this CB Insights report and analyze [COMPANY NAME]'s market entry strategy. Include: initial target market, first products/features launched, early partnerships or distribution channels, pricing approach, and customer acquisition methods. Then assess the effectiveness of their strategy and identify key lessons for a new entrant in the construction tech space.
```

9. **Growth Trajectory Analysis**
```
Based on the CB Insights report, analyze [COMPANY NAME]'s growth trajectory. Include: year-over-year changes in funding, employee count growth, geographic expansion, product line evolution, and market expansion. Identify key inflection points in their growth and the strategic decisions that drove them. What patterns emerge that could inform Constructiv AI's growth planning?
```

10. **Strengths and Vulnerabilities Assessment**
```
From this CB Insights report, conduct a detailed strengths and vulnerabilities assessment for [COMPANY NAME]. Include: core competitive advantages, technological moats, market positioning strengths, resource advantages, as well as operational weaknesses, market gaps, customer pain points they're not addressing, and potential areas for disruption. Provide strategic recommendations on how a competing company could differentiate against them.
```

### Synthesis and Strategy Prompts

11. **Competitive Cluster Analysis**
```
Review the CB Insights reports for these related companies: [LIST 3-5 RELATED COMPANIES]. Analyze how they form a competitive cluster in the construction tech landscape. Include: shared characteristics, collective market focus, common technologies, investment patterns, and how they relate to each other strategically. Then identify the key differentiation factors within this cluster and potential opportunities for a new entrant.
```

12. **Investor Landscape Mapping**
```
Analyze the CB Insights reports for these construction tech companies: [LIST 5+ COMPANIES]. Extract and synthesize information about their investors, including: most active investors in the space, investment patterns (stage preferences, check sizes), strategic vs. financial investors, and recurring investors across multiple companies. Then recommend a targeted list of potential investors that might be suitable for Constructiv AI based on this analysis.
```

13. **Strategic Partnership Opportunity Analysis**
```
Based on these CB Insights reports for [LIST 3-5 COMPANIES], identify and analyze potential strategic partnership opportunities for Constructiv AI. Include: complementary technology providers, distribution partners, integration possibilities, and companies with aligned but non-competing offerings. For each potential partnership type, explain the strategic rationale and potential go-to-market advantages.
```

## Part 2: Excel Template for Organizing Competitive Intelligence

Here's a template structure for organizing your competitive analysis data in Excel. This will help you systematically capture and compare information across companies.

### Excel Workbook Structure

**Worksheet 1: Master Dashboard**
- Company name
- Founding year
- HQ location
- Total funding
- Latest funding round
- Latest valuation
- Employee count
- Competitive cluster (dropdown: Core Competitor, Adjacent Competitor, Potential Partner)
- Primary solution category
- Target customer segment
- Key differentiator
- Strategic threat level (1-5 scale)
- Strategic opportunity level (1-5 scale)

**Worksheet 2: Funding Details**
- Company name
- Total funding
- Funding rounds (count)
- Seed round (date, amount, lead investor)
- Series A (date, amount, lead investor)
- Series B (date, amount, lead investor)
- Series C+ (date, amount, lead investor)
- Other funding (date, amount, type)
- Notable investors
- Funding trajectory notes

**Worksheet 3: Product Offerings**
- Company name
- Primary product category
- Secondary product categories
- Key features/capabilities
- Technological approach
- AI implementation (yes/no, description)
- Mobile capabilities
- Integration capabilities
- Pricing model
- Unique selling proposition
- Product strengths
- Product weaknesses

**Worksheet 4: Market Positioning**
- Company name
- Primary target market
- Secondary markets
- Customer size focus
- Industry specialization
- Geographic focus
- Go-to-market strategy
- Channel partnerships
- Marketing messaging themes
- Customer testimonials focus
- Positioning strengths
- Positioning vulnerabilities

**Worksheet 5: Leadership & Investors**
- Company name
- CEO (name, background)
- Technical leadership (name, background)
- Other key executives
- Board members
- Lead investors
- Strategic investors
- Financial investors
- Advisory board members
- Leadership strengths
- Potential connections to leverage

**Worksheet 6: Competitive Clusters**
- Cluster name
- Companies in cluster
- Cluster defining characteristics
- Total funding in cluster
- Market focus
- Technological commonalities
- Competitive dynamics within cluster
- Key differentiators between companies
- Cluster strengths
- Cluster vulnerabilities
- Opportunity areas

**Worksheet 7: Strategic Analysis**
- Company name
- Key strengths
- Key vulnerabilities
- Market gaps not addressed
- Differentiation strategy
- Technological moat
- Potential disruption vectors
- Partnership potential (1-5)
- Acquisition threat/opportunity (1-5)
- Strategic recommendations
- Monitoring priorities

## Part 3: Automating Excel Creation with AI

To automatically generate this Excel file, you can use this prompt:

```
Based on my analysis of the CB Insights report for [COMPANY NAME], create a structured dataset in CSV format that captures all the key information fields from my Excel template. Format the data so each field is properly separated by commas and can be directly imported into Excel. Include all available fields from the master dashboard, funding details, product offerings, market positioning, leadership & investors, and strategic analysis worksheets.
```

Then for multiple companies:

```
Combine the CSV data from my analyses of [LIST COMPANIES] into a consolidated dataset, ensuring consistent formatting across all entries. Structure the data to align with my Excel template's worksheets, with clear field separators and row organization that will allow for direct import and proper categorization in Excel.
```

## Part 4: Implementation Strategy

1. **Process each report individually** first using prompts 1-10 to extract comprehensive information on each company.

2. **Group related companies** and use prompts 11-13 to analyze competitive clusters and strategic implications.

3. **Generate CSV data** for each company using the automation prompt.

4. **Import the CSV data** into your Excel template, with separate imports for each worksheet.

5. **Refine and enhance** the data manually where needed, particularly for the strategic analysis sections.

6. **Create visualizations** based on the compiled data - competitive positioning maps, funding comparisons, and feature matrices.

7. **Develop strategic recommendations** based on the patterns and insights revealed in your analysis.

This systematic approach will help you transform your CB Insights reports into actionable strategic intelligence that can guide your product development, market positioning, and growth planning for Constructiv AI.
