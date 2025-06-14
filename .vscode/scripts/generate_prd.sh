#!/bin/bash

# Script to generate and update the Product Requirements Document (PRD)

echo "Task-Master AI: Generating Product Requirements Document..."

# Create the docs directory if it doesn't exist
mkdir -p "$(dirname "$0")"/../../docs

# Set variables
PRD_FILE="$(dirname "$0")"/../../docs/product_requirements_document.md
TEMPLATE_FILE="$(dirname "$0")"/../../docs/prd_template.md
TODAY=$(date +"%B %d, %Y")
VERSION=$(date +"%y.%m.%d")

# Check if this is an update or initial creation
if [ -f "$PRD_FILE" ]; then
  echo "Updating existing PRD..."
  # Extract and increment version number
  CURRENT_VERSION=$(grep "Version:" "$PRD_FILE" | sed -E 's/.*Version:\*\* ([0-9]+\.[0-9]+).*/\1/')
  MAJOR_VERSION=$(echo $CURRENT_VERSION | cut -d. -f1)
  MINOR_VERSION=$(echo $CURRENT_VERSION | cut -d. -f2)
  NEW_MINOR_VERSION=$((MINOR_VERSION + 1))
  NEW_VERSION="$MAJOR_VERSION.$NEW_MINOR_VERSION"
  
  # Update the version and date
  sed -i "s/\*\*Last Updated:\*\* .*/\*\*Last Updated:\*\* $TODAY/" "$PRD_FILE"
  sed -i "s/\*\*Version:\*\* .*/\*\*Version:\*\* $NEW_VERSION/" "$PRD_FILE"
  
  echo "PRD updated: Version $NEW_VERSION"
else
  echo "Creating new PRD from template..."
  # If template doesn't exist, the script will exit
  if [ ! -f "$TEMPLATE_FILE" ]; then
    echo "Error: PRD template not found. Using default PRD."
    exit 0
  fi
  
  # Copy template and replace placeholders
  cp "$TEMPLATE_FILE" "$PRD_FILE"
  sed -i "s/{{DATE}}/$TODAY/g" "$PRD_FILE"
  sed -i "s/{{VERSION}}/1.0/g" "$PRD_FILE"
  
  echo "New PRD created: Version 1.0"
fi

# Generate feature analysis based on code structure (simplified)
echo -e "\n## Auto-generated Feature Analysis" >> "$PRD_FILE"
echo -e "\nGenerated on $TODAY by Task-Master AI\n" >> "$PRD_FILE"

# Count features by analyzing code structure
API_COUNT=$(find "$(dirname "$0")"/../../api -name "*.py" | wc -l)
UI_COMPONENTS=$(find "$(dirname "$0")"/../../ui/src/components -name "*.js" | wc -l)
UI_PAGES=$(find "$(dirname "$0")"/../../ui/src/pages -name "*.js" | wc -l)

# Append results to PRD
echo -e "| Feature Area | Implementation Status |" >> "$PRD_FILE"
echo -e "|-------------|----------------------|" >> "$PRD_FILE"
echo -e "| API Endpoints | $API_COUNT implemented |" >> "$PRD_FILE"
echo -e "| UI Components | $UI_COMPONENTS implemented |" >> "$PRD_FILE"
echo -e "| UI Pages | $UI_PAGES implemented |" >> "$PRD_FILE"

echo "Feature analysis added to PRD."
echo "PRD generation complete."
