# Ссылки шаблоны по каждому магазину, которые необходимо отформатировать
# при парсинге вставив в ссылку название товара и номер страницы
URL_WILDBERRIES = "https://www.wildberries.ru/catalog/0/search.aspx?page={page}&sort=popular&search={product}"
URL_ALIEXPRESS = "https://aliexpress.ru/wholesale?SearchText={product}&g=undefined&page={page}"

# Container Wildberries
WILD_NAME_BLOCK = 'product-card j-card-item j-good-for-listing-event'
WILD_NAME_URL = 'product-card__main j-card-link'
WILD_NAME_BRAND = 'brand-name'
WILD_NAME_GOODS = 'goods-name'
WILD_NAME_PRICE = 'lower-price'
WILD_NAME_IMAGE = 'j-thumbnail thumbnail'

# Container Aliexpress
ALI_NAME_BLOCK1 = 'product-snippet_ProductSnippet__container__tusfnx product-snippet_ProductSnippet__horizontal__tusfnx product-snippet_ProductSnippet__imageSizeS__tusfnx product-snippet_ProductSnippet__hasGallery__tusfnx product-snippet_ProductSnippet__hideOptions__tusfnx product-snippet_ProductSnippet__hideCashback__tusfnx product-snippet_ProductSnippet__hideSubsidy__tusfnx product-snippet_ProductSnippet__hideAd__tusfnx product-snippet_ProductSnippet__hideActions__tusfnx product-snippet_ProductSnippet__hideSponsored__tusfnx product-snippet_ProductSnippet__hideGroupLink__tusfnx'
ALI_NAME_BLOCK2 = 'product-snippet_ProductSnippet__container__tusfnx product-snippet_ProductSnippet__vertical__tusfnx product-snippet_ProductSnippet__imageSizeM__tusfnx product-snippet_ProductSnippet__hasGallery__tusfnx product-snippet_ProductSnippet__hideOptions__tusfnx product-snippet_ProductSnippet__hideCashback__tusfnx product-snippet_ProductSnippet__hideSubsidy__tusfnx product-snippet_ProductSnippet__hideAd__tusfnx product-snippet_ProductSnippet__hideActions__tusfnx product-snippet_ProductSnippet__hideSponsored__tusfnx product-snippet_ProductSnippet__hideGroupLink__tusfnx'
ALI_NAME_URL = 'product-snippet_ProductSnippet__galleryBlock__tusfnx'
ALI_NAME_BRAND = 'product-snippet_ProductSnippet__caption__tusfnx'
ALI_NAME_GOODS = 'product-snippet_ProductSnippet__name__tusfnx'
ALI_NAME_PRICE = 'snow-price_SnowPrice__mainM__1ehyuw'
ALI_NAME_IMAGE = 'gallery_Gallery__image__1ln22f'
