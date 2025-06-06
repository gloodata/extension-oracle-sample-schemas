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


# =====================================
# Utilities to create charts and tables
# =====================================
def create_group_chart(title, cols, rows, unit="", chart_type="bar"):
    on_clicks = []
    col_keys = [col[0] for col in cols]
    row_lists = [[row.get(key) for key in col_keys] for row in rows]

    result = {
        "info": {
            "type": "group",
            "chartType": chart_type,
            "title": title,
            "unit": unit,
            "keyName": cols[0][0],
            "valName": cols[1][0],
            "onClick": on_clicks,
        },
        "data": {"cols": cols, "rows": row_lists},
    }
    return result


def create_series_chart(title, cols, rows, chart_type="bar"):
    x, x_title = cols[0]
    serie, serie_title = cols[1]
    y, y_title = cols[2]

    col_keys = [col[0] for col in cols]
    row_lists = [[row.get(key) for key in col_keys] for row in rows]
    on_clicks = []

    return {
        "type": "Series",
        "chartType": chart_type,
        "title": title,
        "unit": "#",
        "xColTitle": x_title,
        "yColTitle": y_title,
        "seriesCol": serie,
        "xCol": x,
        "valCols": [y],
        "pivot": {
            "keyName": serie,
            "valName": y,
        },
        "cols": cols,
        "rows": row_lists,
        "onClick": on_clicks,
    }


def to_area(rows):
    areas = [{"name": row[0], "value": row[1]} for idx, row in enumerate(rows)]
    return areas


def create_area_map(title, cols, rows, map_type="usa"):
    col_keys = [col[0] for col in cols]
    row_lists = [[row.get(key) for key in col_keys] for row in rows]
    areas = to_area(row_lists)
    on_clicks = []
    result = {
        "type": "AreaMap",
        "mapId": map_type,
        "infoId": map_type,
        "onClick": on_clicks,
        "items": areas,
    }
    return result


def create_table(columns, rows):
    on_clicks = []
    rows_values = [[row[col["id"]] for col in columns] for row in rows]
    return {
        "type": "Table",
        "columns": columns,
        "rows": rows_values,
        "onClick": on_clicks,
    }


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

    return create_group_chart(
        "Sales by product category",
        [["category", "Category"], ["total_sales", "total_sales"]],
        rows,
        chart_type="bar",
    )


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

    return create_group_chart(
        "Sales by channel",
        [["channel", "Channel"], ["total_sales", "total_sales"]],
        rows,
        chart_type="bar",
    )


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
    - An pie chart showing customer density by region.
    """
    rows = await state.run_query(
        "customer_density",
        start_date=start_date,
        end_date=end_date,
        customer_segment=customer_segment,
    )

    cols = [["region", "Country"], ["customer_count", "Customer Count"]]
    return create_group_chart("Customer density by region", cols, rows, chart_type="pie")


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

    return create_series_chart(
        "Monthly sales trend by category",
        [["calendar_month_desc", "Month"], ["category", "Category"], ["total_sales", "total_sales"]],
        rows,
        chart_type="line",
    )


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

    return create_series_chart(
        "Quarterly sales by channel",
        [["calendar_quarter_desc", "Quarter"], ["category", "Channel"], ["total_sales", "total_sales"]],
        rows,
        chart_type="line",
    )


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

    columns = [
        {"id": "category", "label": "Category", "visible": True },
        {"id": "country", "label": "Country", "visible": True },
        {"id": "total_sales", "label": "Total Sales", "visible": True },
        {"id": "total_quantity", "label": "Total Quantity", "visible": True },
        {"id": "unique_customers", "label": "Unique Customers", "visible": True },
        {"id": "avg_sale_amount", "label": "Avg Sale Amount", "visible": True },
        {"id": "avg_unit_price", "label": "Avg Unit Price", "visible": True },
    ]

    return create_table(columns, rows)


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

    cols = [["region", "Country"], ["total_sales", "Total Sales"]]
    return create_area_map("Sales by country", cols, rows, map_type="world")
