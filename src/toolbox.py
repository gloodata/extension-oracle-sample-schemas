from glootil import Toolbox, DynEnum
from state import State
import logging
from datetime import date

logger = logging.getLogger("toolbox")
NS = "gd-oracle"
tb = Toolbox(
    NS,
    "Oracle Sample Schema",
    "Oracle Sample Schemas Explorer",
    state=State(config="config.toml"),
)


# ================================
# Declaration of enums and filters
# ================================
@tb.enum(name="country", icon="map")
class Country(DynEnum):
    """
    Represents a country for filtering purposes.
    """

    @staticmethod
    async def search(state: State, query: str = "", limit: int = 100):
        return await state.search("country_enum", query, limit)

    @staticmethod
    async def find_best_match(state: State, query: str = ""):
        return await Country.search(state, query, limit=1)


@tb.enum(name="product_category", icon="tag")
class ProductCategory(DynEnum):
    """
    Represents a product category for filtering purposes.
    """

    @staticmethod
    async def search(state: State, query: str = "", limit: int = 100):
        return await state.search("product_category_enum", query, limit)

    @staticmethod
    async def find_best_match(state: State, query: str = ""):
        return await ProductCategory.search(state, query, limit=1)


@tb.enum(name="channel", icon="share")
class Channel(DynEnum):
    """
    Represents a sales channel for filtering purposes.
    """

    @staticmethod
    async def search(state: State, query: str = "", limit: int = 100):
        return await state.search("channel_enum", query, limit)

    @staticmethod
    async def find_best_match(state: State, query: str = ""):
        return await Channel.search(state, query, limit=1)


@tb.enum(name="customer_segment", icon="users")
class CustomerSegment(DynEnum):
    """
    Represents a customer segment for filtering purposes.
    """

    @staticmethod
    async def search(state: State, query: str = "", limit: int = 100):
        return await state.search("customer_segment_enum", query, limit)

    @staticmethod
    async def find_best_match(state: State, query: str = ""):
        return await CustomerSegment.search(state, query, limit=1)


# ====================
# Declaration of tools
# ====================

# 1. Sales by product category
@tb.tool(
    name="Sales by product category",
    examples=[
        "Sales by product category",
    ],
    manual_update=False,
)
async def sales_by_category(
    state: State,
    start_date: date,
    end_date: date,
    country: Country = None,
):
    """
    Analyzes sales performance by product category within a date range, with an optional country filter.

    Parameters:
    - start_date: Start date filter. Mandatory, default is today minus 1 year.
    - end_date: End date filter. Mandatory, default is today.
    - country: Optional filter to focus the analysis on a specific country.

    Result:
    - A bar chart showing total sales by product category.
    """
    rows = await state.run_query(
        "sales_by_category",
        start_date=start_date,
        end_date=end_date,
        country=country,
    )

    # Convert rows to the expected format
    row_data = [[row["category"], row["total_sales"]] for row in rows]

    return {
        "info": {
            "type": "group",
            "chartType": "bar",
            "title": "Sales by product category",
            "unit": "",
            "keyName": "category",
            "valName": "total_sales",
            "onClick": [],
        },
        "data": {
            "cols": [["category", "Category"], ["total_sales", "total_sales"]],
            "rows": row_data
        },
    }


# 2. Sales by Channel
@tb.tool(
    name="Sales by channel",
    examples=[
        "Sales by channel",
    ],
    manual_update=False,
)
async def sales_by_channel(
    state: State,
    start_date: date,
    end_date: date,
    product_category: ProductCategory = None,
    customer_segment: CustomerSegment = None,
):
    """
    Shows total sales amount by sales channel with optional filters.

    Parameters:
    - start_date: Start date filter.
    - end_date: End date filter.
    - product_category: Optional filter for product category.
    - customer_segment: Optional filter for customer segment.

    Result:
    - A bar chart showing total sales by channel.
    """
    rows = await state.run_query(
        "sales_by_channel",
        start_date=start_date,
        end_date=end_date,
        product_category=product_category,
        customer_segment=customer_segment,
    )

    # Convert rows to the expected format
    row_data = [[row["channel"], row["total_sales"]] for row in rows]

    return {
        "info": {
            "type": "group",
            "chartType": "bar",
            "title": "Sales by channel",
            "unit": "",
            "keyName": "channel",
            "valName": "total_sales",
            "onClick": [],
        },
        "data": {
            "cols": [["channel", "Channel"], ["total_sales", "total_sales"]],
            "rows": row_data
        },
    }


# 3. Customer Density by Region
@tb.tool(
    name="Customer density by region",
    examples=[
        "Customer density by region",
    ],
    manual_update=False,
)
async def customer_density(
    state: State,
    start_date: date,
    end_date: date,
    customer_segment: CustomerSegment = None,
):
    """
    Shows customer count by geographic region for density mapping.

    Parameters:
    - start_date: Start date filter.
    - end_date: End date filter.
    - customer_segment: Optional filter for customer segment.

    Result:
    - A pie chart showing customer density by region.
    """
    rows = await state.run_query(
        "customer_density",
        start_date=start_date,
        end_date=end_date,
        customer_segment=customer_segment,
    )

    # Convert rows to the expected format
    row_data = [[row["region"], row["customer_count"]] for row in rows]

    return {
        "info": {
            "type": "group",
            "chartType": "pie",
            "title": "Customer density by region",
            "unit": "",
            "keyName": "region",
            "valName": "customer_count",
            "onClick": [],
        },
        "data": {
            "cols": [["region", "Country"], ["customer_count", "Customer Count"]],
            "rows": row_data
        },
    }


# 4. Monthly Sales Trend by Category
@tb.tool(
    name="Monthly sales trend by category",
    examples=[
        "Monthly sales trend by category",
    ],
    manual_update=False,
)
async def monthly_sales_trend(
    state: State,
    start_date: date,
    end_date: date,
    country: Country = None,
    product_category: ProductCategory = None,
):
    """
    Shows monthly sales trends by product category over time.

    Parameters:
    - start_date: Start date filter.
    - end_date: End date filter.
    - country: Optional filter for country.
    - product_category: Optional filter for product category.

    Result:
    - A series chart showing monthly sales by category.
    """
    rows = await state.run_query(
        "monthly_sales_trend",
        start_date=start_date,
        end_date=end_date,
        country=country,
        product_category=product_category,
    )

    # Convert rows to the expected format
    row_data = [[row["calendar_month_desc"], row["category"], row["total_sales"]] for row in rows]

    return {
        "type": "Series",
        "chartType": "line",
        "title": "Monthly sales trend by category",
        "unit": "#",
        "xColTitle": "Month",
        "yColTitle": "total_sales",
        "seriesCol": "category",
        "xCol": "calendar_month_desc",
        "valCols": ["total_sales"],
        "pivot": {
            "keyName": "category",
            "valName": "total_sales",
        },
        "cols": [["calendar_month_desc", "Month"], ["category", "Category"], ["total_sales", "total_sales"]],
        "rows": row_data,
        "onClick": [],
    }


@tb.tool(
    name="Quarterly sales by channel",
    examples=[
        "Quarterly sales by channel",
    ],
    manual_update=False,
)
async def quarterly_sales_by_channel(
    state: State,
    start_date: date,
    end_date: date,
    customer_segment: CustomerSegment = None,
    min_amount: float = None,
):
    """
    Shows quarterly sales performance by channel over time.

    Parameters:
    - start_date: Start date filter.
    - end_date: End date filter.
    - customer_segment: Optional filter for customer segment.
    - min_amount: Optional minimum sales amount filter.

    Result:
    - A series chart showing quarterly sales by channel.
    """
    rows = await state.run_query(
        "quarterly_sales_by_channel",
        start_date=start_date,
        end_date=end_date,
        customer_segment=customer_segment,
        min_amount=min_amount,
    )

    # Convert rows to the expected format
    row_data = [[row["calendar_quarter_desc"], row["category"], row["total_sales"]] for row in rows]

    return {
        "type": "Series",
        "chartType": "line",
        "title": "Quarterly sales by channel",
        "unit": "#",
        "xColTitle": "Quarter",
        "yColTitle": "total_sales",
        "seriesCol": "category",
        "xCol": "calendar_quarter_desc",
        "valCols": ["total_sales"],
        "pivot": {
            "keyName": "category",
            "valName": "total_sales",
        },
        "cols": [["calendar_quarter_desc", "Quarter"], ["category", "Channel"], ["total_sales", "total_sales"]],
        "rows": row_data,
        "onClick": [],
    }


@tb.tool(
    name="Comprehensive sales analysis",
    examples=[
        "Comprehensive sales analysis",
    ],
    manual_update=False,
)
async def sales_analysis(
    state: State,
    start_date: date,
    end_date: date,
    product_category: ProductCategory = None,
    country: Country = None,
):
    """
    Shows detailed sales metrics with multiple dimensions.

    Parameters:
    - start_date: Start date filter.
    - end_date: End date filter.
    - product_category: Optional filter for product category.
    - country: Optional filter for country.

    Result:
    - A table with sales metrics by category and country.
    """
    rows = await state.run_query(
        "sales_analysis",
        start_date=start_date,
        end_date=end_date,
        product_category=product_category,
        country=country,
    )

    # Convert rows to the expected format
    row_data = [
        [
            row["category"],
            row["country"],
            row["total_sales"],
            row["total_quantity"],
            row["unique_customers"],
            row["avg_sale_amount"],
            row["avg_unit_price"]
        ]
        for row in rows
    ]

    return {
        "type": "Table",
        "columns": [
            {"id": "category", "label": "Category", "visible": True},
            {"id": "country", "label": "Country", "visible": True},
            {"id": "total_sales", "label": "Total Sales", "visible": True},
            {"id": "total_quantity", "label": "Total Quantity", "visible": True},
            {"id": "unique_customers", "label": "Unique Customers", "visible": True},
            {"id": "avg_sale_amount", "label": "Avg Sale Amount", "visible": True},
            {"id": "avg_unit_price", "label": "Avg Unit Price", "visible": True},
        ],
        "rows": row_data,
        "onClick": [],
    }


@tb.tool(
    name="Sales by country (geographic)",
    examples=[
        "Sales by country",
    ],
    manual_update=False,
)
async def sales_by_country(
    state: State,
    start_date: date,
    end_date: date,
    product_category: ProductCategory = None,
    min_sales: float = None,
):
    """
    Provides sales data by country for geographic visualization.

    Parameters:
    - start_date: Start date filter.
    - end_date: End date filter.
    - product_category: Optional filter for product category.
    - min_sales: Optional minimum sales amount filter.

    Result:
    - An area map showing total sales by country.
    """
    rows = await state.run_query(
        "sales_by_country",
        start_date=start_date,
        end_date=end_date,
        product_category=product_category,
        min_sales=min_sales,
    )

    # Convert rows to the expected format
    items = [{"name": row["region"], "value": row["total_sales"]} for row in rows]

    return {
        "type": "AreaMap",
        "mapId": "world",
        "infoId": "world",
        "onClick": [],
        "items": items,
    }