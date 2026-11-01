# 🚀 Oostervelde Invoice Auditor - Setup Guide

Follow these steps to connect the local MCP server and install the custom invoice auditing skill into your Claude Desktop client.

## 🛠️ Step 1: Clone & Install Dependencies
First, clone or pull this repository to your local machine and install the required Python libraries.
```bash
pip install -r requirements.txt
```

## ⚙️ Step 2: Configure Claude Desktop MCP Server
You need to tell Claude Desktop where your local server lives. 
1. Open your Claude Desktop configuration file (usually found at `%APPDATA%\Claude\claude_desktop_config.json` on Windows). Alternatively, go to `Claude Desktop > Settings > Storage > Manage > Open Folder` and open the `claude_desktop_config.json` file
2. Add your local server to the `mcpServers` object, pointing to your project directory.
3. It should look something like this:

```json
{
  "mcpServers": {
    "accounting-mcp-server": {
      "command": "C:\\Users\\zero\\projects\\accounting-mcp-server\\venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\zero\\projects\\accounting-mcp-server\\server.py"
      ]
    }
  }
}

```

## 🧠 Step 3: Install the Custom Skill in Claude Desktop
Because Claude Desktop runs in a sandboxed environment, custom skills must be added directly via the user interface.

1. Open your **Claude Desktop Client**.
2. Navigate to the **Skills / Plugins** tab (or click **Customize** in the sidebar).
3. Click **Create New Skill**.
4. Open the local mcp server folder `.claude/skills/audit-invoices-skill.md` and copy its contents.
5. Paste the respective fields into the UI:
   * **Name:** `oostervelde-invoice-auditor`
   * **Description:** `Triggers when the user asks to process, audit, or review contractor invoices for the Oostervelde project, calculate financial variances, verify contract compliance under Article 4, or generate a review list for Sanne.`
   * **Instructions / Contents:** *(Paste the full step-by-step rules matrix and formatting rules)*
6. Click **Save**.

## 🏃‍♂️ Step 4: Run a Test Pass
Open a brand new chat window in Claude Desktop and paste the sample prompt below to verify the MCP tools and the skill formatting are working seamlessly together.

**Sample Prompt:**
> "Using the oostervelde-invoice-auditor skill, process only these 10 specific files sequentially: h-2026-0031.txt, w-DW26-004.txt, j-F26-0007.txt, h-2026-0038.txt, b-B-26-0102.txt, w-DW26-009.txt, h-2026-0044.txt, w-DW26-011.txt, j-F26-0012.txt, b-B-26-0097.txt found on the data/invoices folder and follow the instructions and layout on the skill."
