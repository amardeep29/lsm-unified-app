# 🖼️ Image Gallery Feature Guide

## Overview

The **Image Gallery** is a new tab in the Streamlit web application that allows users to browse, search, and manage all images stored in Cloudinary across different client folders. This feature provides a comprehensive view of your entire image library with powerful filtering, pagination, and export capabilities.

## Features

### 1. Client Folder Selection
- **Dropdown selector** displays all available client folders from Cloudinary
- Dynamically loads folder list on page load
- Supports multiple clients in the same Cloudinary account

### 2. Image Type Filtering
Filter images by type:
- **All**: Shows all images (both generated and edited)
- **Generated**: Shows only AI-generated images
- **Edited**: Shows only AI-edited images

### 3. Pagination
- **Configurable page size**: 20, 30, or 50 images per page
- **Previous/Next navigation** for browsing large image sets
- **Page counter** shows current page number
- Efficient cursor-based pagination from Cloudinary API

### 4. Date Range Filtering
- **Start Date**: Filter images created on or after this date
- **End Date**: Filter images created on or before this date
- **Optional**: Leave blank to show all dates
- Real-time filtering applied to results

### 5. Image Grid Display
- **3-column grid layout** for optimal viewing
- **Thumbnail preview** of each image
- **Metadata display** for each image:
  - Filename
  - Dimensions (width × height)
  - Upload date and time
  - Cloudinary URL (copy-ready)

### 6. Image Details
- **Expandable details panel** for each image showing:
  - Public ID
  - Format (PNG, JPG, etc.)
  - File size in bytes
  - Resource type

### 7. Bulk Export
- **Export All URLs** button generates CSV file with:
  - Filename
  - Full Cloudinary URL
  - Width
  - Height
  - Created date
  - Public ID
- **Download CSV** instantly downloads the export file
- Filename format: `cloudinary_export_{client}_{timestamp}.csv`

### 8. Reset Filters
- **Reset button** clears all filters and reloads from first page
- Returns to page 1 with default settings

## Usage

### Accessing the Gallery

1. Open the Streamlit app: `streamlit run app.py`
2. Navigate to the **🖼️ Image Gallery** tab
3. The gallery will automatically load available client folders

### Basic Browsing

1. **Select a client folder** from the dropdown
2. Choose **image type** (all, generated, or edited)
3. Set **images per page** (20, 30, or 50)
4. Images will load automatically in a grid

### Filtering by Date

1. Click on **Start Date** calendar picker
2. Select the earliest date you want to see
3. Optionally set **End Date** for upper limit
4. Images will filter automatically

**Example:**
```
Start Date: 2025-10-01
End Date: 2025-10-07
Result: Only images from October 1-7, 2025
```

### Navigating Pages

- **Previous Page** (⬅️): Go back one page (if not on page 1)
- **Next Page** (➡️): Go forward one page (if more images available)
- **Page indicator**: Shows current page number

### Viewing Image Details

1. Locate the image in the grid
2. Find the **ℹ️ Details** expander below the image
3. Click to expand and see technical details

### Copying Image URLs

Each image displays its Cloudinary URL in a code block. You can:
- **Click** to select the entire URL
- **Copy** using Ctrl+C (Cmd+C on Mac)
- **Paste** wherever needed

### Exporting URLs in Bulk

1. Apply desired filters (client, type, dates)
2. Click **📤 Export All URLs** button
3. Click **💾 Download CSV** button that appears
4. CSV file downloads with all filtered images

**CSV Format:**
```csv
filename,url,width,height,created_at,public_id
generated_1728345678,https://res.cloudinary.com/.../image.png,1024,1024,2025-10-07T12:34:56Z,client/generated/generated_1728345678
```

## Technical Implementation

### CloudinaryManager Methods

#### `list_client_folders()`
```python
folders_result = cloudinary_client.list_client_folders()
# Returns: {'success': True, 'folders': ['ClientA', 'ClientB', 'ClientC']}
```

#### `list_images_paginated()`
```python
result = cloudinary_client.list_images_paginated(
    client_folder="ClientA",
    folder_type="all",
    max_results=30,
    next_cursor=None,
    start_date="2025-10-01",
    end_date="2025-10-07"
)
```

**Returns:**
```python
{
    'success': True,
    'images': [...],  # List of image objects
    'total_count': 150,
    'next_cursor': 'abc123...',
    'has_more': True
}
```

### Session State Variables

The gallery uses the following session state variables:

- `gallery_page_cursor`: Cloudinary pagination cursor
- `gallery_current_page`: Current page number (display only)
- `gallery_client_selector`: Selected client folder
- `gallery_folder_type`: Selected image type filter
- `gallery_per_page`: Images per page setting
- `gallery_start_date`: Start date filter value
- `gallery_end_date`: End date filter value

## Cloudinary Folder Structure

The gallery expects this folder structure in Cloudinary:

```
cloudinary_root/
├── ClientA/
│   ├── generated/
│   │   ├── generated_1728345678.png
│   │   └── generated_1728345679.png
│   ├── edited/
│   │   ├── edited_1728345680.png
│   │   └── edited_1728345681.png
│   └── input/
│       └── input_1728345682.png
├── ClientB/
│   ├── generated/
│   └── edited/
└── ClientC/
    ├── generated/
    └── edited/
```

## Use Cases

### 1. Marketing Asset Management
**Scenario**: Marketing team needs to find all campaign images from last month

**Steps**:
1. Select client folder: "BrandXYZ"
2. Set date range: October 1-31, 2025
3. Export URLs to CSV
4. Share CSV with team for asset selection

### 2. Quality Assurance Review
**Scenario**: Review all generated images for a client before delivery

**Steps**:
1. Select client folder: "ClientABC"
2. Set type: "generated"
3. Browse through pages
4. Check dimensions and quality
5. Note any issues

### 3. Content Audit
**Scenario**: Audit total image count and storage usage

**Steps**:
1. Select client folder
2. Set type: "all"
3. Note total count displayed
4. Export CSV for detailed analysis
5. Review file sizes in CSV

### 4. Historical Image Search
**Scenario**: Find image created around a specific date

**Steps**:
1. Select client folder
2. Set date range around target date
3. Browse thumbnails to identify image
4. Copy URL for use

### 5. Bulk URL Collection
**Scenario**: Need URLs for all product mockup images

**Steps**:
1. Select client folder: "ProductTeam"
2. Set type: "edited"
3. Click "Export All URLs"
4. Download CSV
5. Import into product management system

## Performance Considerations

### Pagination Strategy
- **Cursor-based pagination**: More efficient than offset-based for large datasets
- **Lazy loading**: Images loaded on demand per page
- **API call optimization**: Single call per page load

### Image Loading
- **Cloudinary CDN**: Images served from Cloudinary's global CDN
- **Thumbnail optimization**: Cloudinary automatically optimizes image delivery
- **Browser caching**: Repeated views load faster

### Filter Performance
- **Date filtering**: Applied after fetch (client-side filtering)
- **Type filtering**: Applied in query (server-side filtering)
- **Recommendation**: Use specific filters to reduce result set

## Troubleshooting

### No Client Folders Shown

**Problem**: Dropdown shows "No client folders found"

**Solutions**:
1. Verify images have been generated/uploaded
2. Check Cloudinary credentials in `.env`
3. Ensure folder structure follows convention
4. Generate test image to create folder

### Images Not Loading

**Problem**: Grid shows loading spinner indefinitely

**Solutions**:
1. Check browser console for errors
2. Verify Cloudinary API key permissions
3. Check network connectivity
4. Try refreshing the page

### Pagination Not Working

**Problem**: "Next Page" button doesn't appear

**Causes**:
- All images fit on one page
- No more images available
- API error occurred

**Solutions**:
1. Check total count vs. per-page setting
2. Review error messages at top of page
3. Try resetting filters

### Date Filter Not Working

**Problem**: Same images shown regardless of date

**Causes**:
- Images don't have creation dates
- Date range too broad
- Client-side filtering issue

**Solutions**:
1. Check image metadata has `created_at` field
2. Narrow date range
3. Reset and try again

### Export CSV Empty

**Problem**: CSV downloads but has no data

**Causes**:
- No images match current filters
- API returned empty result
- Permission issue

**Solutions**:
1. Remove date filters and try again
2. Check image count indicator
3. Try different client folder

## API Reference

### Cloudinary API Methods Used

#### `api.root_folders()`
Lists all top-level folders in Cloudinary account.

#### `api.resources()`
Lists resources (images) with filtering options:
- `type`: Resource type (upload, private, etc.)
- `prefix`: Folder path filter
- `max_results`: Pagination limit
- `next_cursor`: Pagination cursor
- `resource_type`: image, video, raw, etc.

## Future Enhancements

Potential additions to the gallery feature:

1. **Image Preview Modal**: Full-size image viewer with navigation
2. **Bulk Delete**: Select and delete multiple images
3. **Tags Support**: Add/edit tags for image organization
4. **Advanced Search**: Search by filename or metadata
5. **Folder Management**: Create/rename/delete client folders
6. **Image Upload**: Upload images directly to gallery
7. **Batch Download**: Download multiple images as ZIP
8. **Image Comparison**: Side-by-side comparison view
9. **Sorting Options**: Sort by date, size, name
10. **Grid Size Options**: 2, 3, or 4 column layouts

## Best Practices

### Organization
- Use consistent client folder naming
- Separate generated and edited images
- Document naming conventions in team docs

### Performance
- Use date filters for large image sets
- Keep page size reasonable (30 recommended)
- Export CSVs rather than loading all images

### Workflow
- Review new images daily via gallery
- Export CSVs for record keeping
- Use filters to focus on specific content

### Security
- Don't share Cloudinary credentials
- Use environment variables for API keys
- Limit access to sensitive client folders

---

**Feature Version**: 1.0.0
**Added**: October 2025
**Compatible With**: Streamlit App v1.0+, Cloudinary API v1.0+
