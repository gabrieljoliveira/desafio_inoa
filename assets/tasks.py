import yfinance as yf

from celery import shared_task

from .models import Asset, AssetData


@shared_task
def get_asset_data(**kwargs):
    asset_name = kwargs["asset_name"]
    user_asset = Asset.objects.get(name=asset_name, created_by=kwargs["created_by"])
    asset_info = yf.Ticker(asset_name)
    asset_data = AssetData(asset=user_asset, value=asset_info.info["currentPrice"])
    asset_data.save()
