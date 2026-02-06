#!/usr/bin/env python3
"""
Update Google Docs agreements:
1. Update "Agreement - Leads (Template)" with guaranteed leads content
2. Update/create "Lead Generation Agreement (Budget Campaign) — Template" with budget version
"""

import json
import sys
import urllib.request
import urllib.parse
import urllib.error

# ─── Auth ───────────────────────────────────────────────────────────────────

def get_access_token():
    with open('/home/ec2-user/.config/gcal-pro/token.json') as f:
        token_data = json.load(f)
    
    data = urllib.parse.urlencode({
        'client_id': token_data['client_id'],
        'client_secret': token_data['client_secret'],
        'refresh_token': token_data['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
    
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data)
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    return result['access_token']

def api_request(url, method='GET', data=None, token=None):
    if data is not None:
        data = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Authorization', f'Bearer {token}')
    if data is not None:
        req.add_header('Content-Type', 'application/json')
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode()}", file=sys.stderr)
        raise

# ─── Markdown to Google Docs requests ──────────────────────────────────────

def parse_markdown_to_requests(md_text):
    """Convert markdown text to Google Docs API batchUpdate requests."""
    lines = md_text.split('\n')
    requests = []
    current_index = 1  # Google Docs index starts at 1
    
    # Track formatting to apply after all text is inserted
    format_requests = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Check for table
        if '|' in line and line.strip().startswith('|'):
            table_lines = []
            while i < len(lines) and '|' in lines[i] and lines[i].strip().startswith('|'):
                # Skip separator lines
                stripped = lines[i].strip()
                if stripped.replace('|', '').replace('-', '').replace(' ', '') == '':
                    i += 1
                    continue
                cells = [c.strip() for c in stripped.split('|')[1:-1]]
                table_lines.append(cells)
                i += 1
            
            if table_lines:
                num_rows = len(table_lines)
                num_cols = max(len(row) for row in table_lines) if table_lines else 1
                
                # Insert table
                requests.append({
                    'insertTable': {
                        'rows': num_rows,
                        'columns': num_cols,
                        'location': {'index': current_index}
                    }
                })
                # We need to calculate the table index offsets
                # After inserting a table, the indices shift significantly
                # For simplicity, let's insert tables as formatted text instead
                # Actually, tables in Google Docs API are complex. Let's render as text.
                requests.pop()  # Remove the insertTable request
                
                # Render table as formatted text
                for row_idx, row in enumerate(table_lines):
                    text = ' | '.join(row) + '\n'
                    requests.append({
                        'insertText': {
                            'location': {'index': current_index},
                            'text': text
                        }
                    })
                    if row_idx == 0:
                        # Bold the header row
                        format_requests.append({
                            'updateTextStyle': {
                                'range': {
                                    'startIndex': current_index,
                                    'endIndex': current_index + len(text) - 1
                                },
                                'textStyle': {'bold': True},
                                'fields': 'bold'
                            }
                        })
                    current_index += len(text)
                
                # Add blank line after table
                requests.append({
                    'insertText': {
                        'location': {'index': current_index},
                        'text': '\n'
                    }
                })
                current_index += 1
            continue
        
        # Horizontal rule
        if line.strip() == '---':
            text = '———\n\n'
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': text
                }
            })
            current_index += len(text)
            i += 1
            continue
        
        # Headings
        if line.startswith('# '):
            heading_text = line[2:].strip() + '\n'
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': heading_text
                }
            })
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': current_index,
                        'endIndex': current_index + len(heading_text)
                    },
                    'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                    'fields': 'namedStyleType'
                }
            })
            current_index += len(heading_text)
            i += 1
            continue
        
        if line.startswith('## '):
            heading_text = line[3:].strip() + '\n'
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': heading_text
                }
            })
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': current_index,
                        'endIndex': current_index + len(heading_text)
                    },
                    'paragraphStyle': {'namedStyleType': 'HEADING_2'},
                    'fields': 'namedStyleType'
                }
            })
            current_index += len(heading_text)
            i += 1
            continue
        
        if line.startswith('### '):
            heading_text = line[4:].strip() + '\n'
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': heading_text
                }
            })
            format_requests.append({
                'updateParagraphStyle': {
                    'range': {
                        'startIndex': current_index,
                        'endIndex': current_index + len(heading_text)
                    },
                    'paragraphStyle': {'namedStyleType': 'HEADING_3'},
                    'fields': 'namedStyleType'
                }
            })
            current_index += len(heading_text)
            i += 1
            continue
        
        # Bullet list items
        if line.startswith('- '):
            bullet_text = line[2:].strip() + '\n'
            # Handle bold within bullets
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': bullet_text
                }
            })
            # Apply bullet formatting
            format_requests.append({
                'createParagraphBullets': {
                    'range': {
                        'startIndex': current_index,
                        'endIndex': current_index + len(bullet_text)
                    },
                    'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                }
            })
            # Handle inline bold (**text**)
            apply_inline_bold(bullet_text, current_index, format_requests)
            current_index += len(bullet_text)
            i += 1
            continue
        
        # Empty line
        if line.strip() == '':
            requests.append({
                'insertText': {
                    'location': {'index': current_index},
                    'text': '\n'
                }
            })
            current_index += 1
            i += 1
            continue
        
        # Regular text (may contain bold)
        text = line + '\n'
        requests.append({
            'insertText': {
                'location': {'index': current_index},
                'text': text
            }
        })
        # Handle inline bold
        apply_inline_bold(text, current_index, format_requests)
        current_index += len(text)
        i += 1
    
    return requests + format_requests

def apply_inline_bold(text, start_index, format_requests):
    """Find **bold** patterns in text and add formatting requests."""
    import re
    for match in re.finditer(r'\*\*(.+?)\*\*', text):
        # The bold markers are in the text, we need to note their positions
        # But we're inserting text WITH the ** markers... we need to strip them
        pass
    # Actually, we should strip ** from the text before inserting
    # This requires a different approach - let's handle it at a higher level


def markdown_to_plain_with_formatting(md_text):
    """
    Convert markdown to plain text + formatting instructions.
    Returns (plain_text, formatting_list) where formatting_list contains
    (start, end, style) tuples.
    """
    import re
    
    lines = md_text.split('\n')
    result_lines = []
    formatting = []  # (line_idx, type, extra_data)
    
    for line in lines:
        if line.startswith('# '):
            result_lines.append(line[2:])
            formatting.append((len(result_lines)-1, 'HEADING_1', None))
        elif line.startswith('## '):
            result_lines.append(line[3:])
            formatting.append((len(result_lines)-1, 'HEADING_2', None))
        elif line.startswith('### '):
            result_lines.append(line[4:])
            formatting.append((len(result_lines)-1, 'HEADING_3', None))
        elif line.startswith('- '):
            result_lines.append(line[2:])
            formatting.append((len(result_lines)-1, 'BULLET', None))
        elif line.strip() == '---':
            result_lines.append('———')
            formatting.append((len(result_lines)-1, 'HR', None))
        else:
            result_lines.append(line)
    
    return result_lines, formatting


def build_update_requests(md_text, doc_end_index):
    """Build batchUpdate requests to clear doc and insert markdown content."""
    import re
    
    requests = []
    
    # Step 1: Clear existing content (delete from index 1 to end)
    if doc_end_index > 1:
        requests.append({
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': doc_end_index - 1
                }
            }
        })
    
    # Step 2: Process markdown into lines with metadata
    lines = md_text.rstrip('\n').split('\n')
    
    # Build the full plain text (strip markdown syntax)
    processed_lines = []
    line_meta = []  # (type, original_line)
    
    for line in lines:
        if line.startswith('### '):
            processed_lines.append(line[4:])
            line_meta.append('HEADING_3')
        elif line.startswith('## '):
            processed_lines.append(line[3:])
            line_meta.append('HEADING_2')
        elif line.startswith('# '):
            processed_lines.append(line[2:])
            line_meta.append('HEADING_1')
        elif line.startswith('- '):
            processed_lines.append(line[2:])
            line_meta.append('BULLET')
        elif line.strip() == '---':
            processed_lines.append('———')
            line_meta.append('HR')
        else:
            processed_lines.append(line)
            line_meta.append('NORMAL')
    
    # Strip ** from text for insertion, track bold ranges
    full_text_parts = []
    bold_ranges = []
    current_pos = 1  # Start index in doc
    
    for idx, line in enumerate(processed_lines):
        # Process bold markers
        clean_line = ''
        pos_in_line = 0
        line_start = current_pos + len('\n'.join(full_text_parts)) if full_text_parts else current_pos
        
        # Calculate actual start position
        if full_text_parts:
            line_start = 1 + len('\n'.join(full_text_parts)) + 1  # +1 for the newline
        else:
            line_start = 1
        
        parts = re.split(r'(\*\*.*?\*\*)', line)
        clean_parts = []
        offset = line_start
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                inner = part[2:-2]
                bold_ranges.append((offset, offset + len(inner)))
                clean_parts.append(inner)
                offset += len(inner)
            else:
                clean_parts.append(part)
                offset += len(part)
        
        full_text_parts.append(''.join(clean_parts))
    
    full_text = '\n'.join(full_text_parts)
    
    # Recalculate bold ranges with correct positions
    bold_ranges = []
    current_pos = 1
    for idx, line in enumerate(processed_lines):
        parts = re.split(r'(\*\*.*?\*\*)', line)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                inner = part[2:-2]
                bold_ranges.append((current_pos, current_pos + len(inner)))
                current_pos += len(inner)
            else:
                current_pos += len(part)
        current_pos += 1  # newline
    
    # Strip ** from full text
    clean_full_text = re.sub(r'\*\*(.+?)\*\*', r'\1', full_text)
    
    # Insert all text at once
    requests.append({
        'insertText': {
            'location': {'index': 1},
            'text': clean_full_text
        }
    })
    
    # Apply formatting
    # Calculate line positions in the clean text
    clean_lines = clean_full_text.split('\n')
    current_pos = 1
    
    for idx, (line, meta) in enumerate(zip(clean_lines, line_meta)):
        line_end = current_pos + len(line)
        
        if meta == 'HEADING_1':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_pos, 'endIndex': line_end + 1},
                    'paragraphStyle': {'namedStyleType': 'HEADING_1'},
                    'fields': 'namedStyleType'
                }
            })
        elif meta == 'HEADING_2':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_pos, 'endIndex': line_end + 1},
                    'paragraphStyle': {'namedStyleType': 'HEADING_2'},
                    'fields': 'namedStyleType'
                }
            })
        elif meta == 'HEADING_3':
            requests.append({
                'updateParagraphStyle': {
                    'range': {'startIndex': current_pos, 'endIndex': line_end + 1},
                    'paragraphStyle': {'namedStyleType': 'HEADING_3'},
                    'fields': 'namedStyleType'
                }
            })
        elif meta == 'BULLET':
            requests.append({
                'createParagraphBullets': {
                    'range': {'startIndex': current_pos, 'endIndex': line_end + 1},
                    'bulletPreset': 'BULLET_DISC_CIRCLE_SQUARE'
                }
            })
        
        current_pos = line_end + 1  # +1 for newline
    
    # Apply bold formatting
    for start, end in bold_ranges:
        if start < end:
            requests.append({
                'updateTextStyle': {
                    'range': {'startIndex': start, 'endIndex': end},
                    'textStyle': {'bold': True},
                    'fields': 'bold'
                }
            })
    
    return requests


def get_doc_end_index(token, doc_id):
    """Get the end index of a document's body content."""
    doc = api_request(
        f'https://docs.googleapis.com/v1/documents/{doc_id}',
        token=token
    )
    # The end index is the last element's endIndex
    body = doc.get('body', {}).get('content', [])
    if body:
        return body[-1].get('endIndex', 1)
    return 1


def update_doc_with_markdown(token, doc_id, md_text, doc_name):
    """Clear a Google Doc and replace with markdown content."""
    print(f"\n{'='*60}")
    print(f"Updating: {doc_name}")
    print(f"Doc ID: {doc_id}")
    
    # Get current doc end index
    end_index = get_doc_end_index(token, doc_id)
    print(f"Current doc end index: {end_index}")
    
    # Build update requests
    update_requests = build_update_requests(md_text, end_index)
    
    # Execute batch update
    result = api_request(
        f'https://docs.googleapis.com/v1/documents/{doc_id}:batchUpdate',
        method='POST',
        data={'requests': update_requests},
        token=token
    )
    
    print(f"✅ Successfully updated: {doc_name}")
    print(f"   URL: https://docs.google.com/document/d/{doc_id}/edit")
    return result


def create_budget_agreement(guaranteed_md):
    """Derive budget campaign agreement from guaranteed leads agreement."""
    import re
    
    text = guaranteed_md
    
    # 1. Title change
    text = text.replace(
        '# Lead Generation Agreement (Form Fill Leads)',
        '# Lead Generation Agreement (Budget Campaign)'
    )
    
    # 2. Section 3 - PRICING changes
    text = text.replace(
        '## 3. PRICING & GUARANTEE',
        '## 3. PRICING & CAMPAIGN BUDGET'
    )
    text = text.replace(
        '**Investment:** {{contact.custom_field.budget}}',
        '**Campaign Budget:** {{contact.custom_field.budget}}'
    )
    text = text.replace(
        '**Guaranteed Leads:** {{contact.custom_field.guaranteed_leads}}',
        '**Estimated Lead Volume:** {{contact.custom_field.estimated_leads}}'
    )
    text = text.replace(
        '**Expected Delivery:** {{contact.custom_field.delivery_timeline}}',
        '**Expected Delivery Window:** {{contact.custom_field.delivery_timeline}}'
    )
    text = text.replace(
        '**Prepayment:** Full investment amount is due prior to campaign launch.',
        '**Prepayment:** Full campaign budget is due prior to campaign launch.'
    )
    
    # Replace the GUARANTEE section with BUDGET CAMPAIGN TERMS
    guarantee_section = """**THE GUARANTEE:** Provider guarantees delivery of the specified number of Leads for the stated investment. If Provider does not deliver the guaranteed number of Leads, Provider will continue delivering Leads at Provider's cost until the guarantee is fulfilled.

Expected Delivery is an estimate, not a guarantee. Actual delivery timeline may vary based on campaign performance and market conditions.

This is a lead-count guarantee only. No refunds will be issued; all performance adjustments are made via additional lead delivery."""
    
    budget_section = """**BUDGET CAMPAIGN TERMS:** This is a budget-based campaign. Provider will allocate the full campaign budget toward lead generation advertising and delivery. The estimated lead volume above is a projection based on current campaign performance and market conditions — it is not a guarantee.

Actual lead volume may vary based on factors including but not limited to: advertising platform performance, market competition, geographic demand, and seasonal fluctuations.

Provider will optimize campaigns throughout the engagement to maximize lead volume and quality within the stated budget. No refunds will be issued for unused budget once the campaign has launched."""
    
    text = text.replace(guarantee_section, budget_section)
    
    # 3. Section 4 - DISQUALIFICATION changes
    text = text.replace(
        'for it to be excluded from the guaranteed count.',
        'for it to be reviewed.'
    )
    text = text.replace(
        'Leads are only replaced for the above criteria.',
        'Leads are only eligible for replacement consideration for the above criteria.'
    )
    
    # Add replacement best-effort language after 4.3
    text = text.replace(
        'Disqualification requests must be submitted via email to sierra@kuriosbrand.com with Lead ID and reason.',
        'Disqualification requests must be submitted via email to sierra@kuriosbrand.com with Lead ID and reason.\n\n### 4.4 Replacement\nDisqualified leads will be replaced on a best-effort basis within remaining campaign budget. Replacement is not guaranteed and is subject to available budget and campaign capacity.'
    )
    
    # 4. Section 5 - DELIVERY: Add API
    text = text.replace(
        'Leads will be delivered via method agreed upon during onboarding (email, CRM injection, webhook, or other mutually agreed method).',
        'Leads will be delivered via method agreed upon during onboarding (email, CRM injection, webhook, API, or other mutually agreed method).'
    )
    
    # 5. Section 10 - TERM changes
    text = text.replace(
        'This Agreement begins on the Effective Date and continues until the guaranteed Lead volume is delivered.',
        'This Agreement begins on the Effective Date and continues until the campaign budget has been fully allocated and all resulting leads have been delivered.'
    )
    
    # Add early termination clause after the termination paragraph
    text = text.replace(
        'Either Party may terminate this Agreement for material breach that is not cured within five (5) business days after written notice.',
        'Either Party may terminate this Agreement for material breach that is not cured within five (5) business days after written notice.\n\nIf Client terminates prior to full budget allocation, any unspent portion will be refunded minus advertising costs already committed or spent.'
    )
    
    # 6. Section 13 - Add no guarantee of volumes
    text = text.replace(
        "Provider does not guarantee specific conversion rates, signed cases, or revenue outcomes.",
        "Provider does not guarantee specific lead volumes, conversion rates, signed cases, or revenue outcomes."
    )
    
    return text


def main():
    token = get_access_token()
    print(f"✅ Got access token")
    
    # Read source agreement
    with open('/home/ec2-user/clawd/data/agreements/lead-gen-agreement-guaranteed-leads.md') as f:
        guaranteed_md = f.read()
    
    print(f"✅ Read guaranteed leads agreement ({len(guaranteed_md)} chars)")
    
    # ─── TASK 1: Update guaranteed agreement template ───────────────────
    print("\n" + "="*60)
    print("TASK 1: Update Guaranteed Agreement Template")
    print("="*60)
    
    doc_id = '1OhZtLUQGJKex4sbMCTrgrekXX1x3pfwX_g5WaHBoG40'
    doc_name = 'Agreement - Leads (Template)'
    
    update_doc_with_markdown(token, doc_id, guaranteed_md, doc_name)
    
    # ─── TASK 2: Create/Update Budget Campaign Agreement ────────────────
    print("\n" + "="*60)
    print("TASK 2: Create/Update Budget Campaign Agreement")
    print("="*60)
    
    # Generate budget version
    budget_md = create_budget_agreement(guaranteed_md)
    
    # Save locally
    with open('/home/ec2-user/clawd/data/agreements/lead-gen-agreement-general-budget.md', 'w') as f:
        f.write(budget_md)
    print(f"✅ Saved budget agreement locally ({len(budget_md)} chars)")
    
    # Update existing budget campaign template
    budget_doc_id = '1u8i7_1rBAZcS6oW_VreTfPmxuwMlYbE7VbLSIaGXX6E'
    budget_doc_name = 'Lead Generation Agreement (Budget Campaign) — Template'
    
    update_doc_with_markdown(token, budget_doc_id, budget_md, budget_doc_name)
    
    # Rename to match requested name
    rename_data = {'name': 'Lead Generation Agreement (General - Budget Campaign)'}
    api_request(
        f'https://www.googleapis.com/drive/v3/files/{budget_doc_id}',
        method='PATCH',
        data=rename_data,
        token=token
    )
    print(f"✅ Renamed to: Lead Generation Agreement (General - Budget Campaign)")
    
    # ─── Summary ────────────────────────────────────────────────────────
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\nTask 1 - Updated guaranteed agreement:")
    print(f"  Doc: {doc_name}")
    print(f"  URL: https://docs.google.com/document/d/{doc_id}/edit")
    print(f"\nTask 2 - Updated budget campaign agreement:")
    print(f"  Doc: Lead Generation Agreement (General - Budget Campaign)")
    print(f"  URL: https://docs.google.com/document/d/{budget_doc_id}/edit")
    print(f"  Local: /home/ec2-user/clawd/data/agreements/lead-gen-agreement-general-budget.md")


if __name__ == '__main__':
    main()
