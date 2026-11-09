package app.template.patches.amazon.removeads

import app.morphe.patcher.Fingerprint

// Normal (non-jumpstarted) page loads
internal val MShopWebViewClientOnPageFinishedFingerprint = Fingerprint(
    definingClass = "Lcom/amazon/mShop/web/MShopWebViewClient;",
    name = "onPageFinished",
    returnType = "V",
    parameters = listOf("Landroid/webkit/WebView;", "Ljava/lang/String;"),
    strings = listOf("onPageFinished_withDuration"),
)

// Early commit hook so sponsored ads are hidden before the page completes loading
internal val MShopWebViewClientOnPageCommitVisibleFingerprint = Fingerprint(
    definingClass = "Lcom/amazon/mShop/web/MShopWebViewClient;",
    name = "onPageCommitVisible",
    returnType = "V",
    parameters = listOf("Landroid/webkit/WebView;", "Ljava/lang/String;"),
)

// All pages (normal + jumpstarted): fires when WebView is assigned to the fragment
internal val InteractionWebFragmentSetWebViewFingerprint = Fingerprint(
    definingClass = "Lcom/amazon/mShop/web/InteractionWebFragment;",
    name = "setWebView",
    returnType = "V",
    parameters = listOf("Lcom/amazon/mShop/web/MShopWebView;"),
)
