from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

# Create a QApplication instance
app = QApplication([])

# Create a QWebEngineView instance
view = QWebEngineView()

# Load the webpage in QWebEngineView
url = QUrl('https://www.facebook.com/')
view.load(url)

# CSS selector of the elements to hide
css_selector1 = '.xb57i2i.x1q594ok.x5lxg6s.x78zum5.xdt5ytf.x6ikm8r.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.x1l7klhg.x1iyjqo2.xs83m0k.x2lwn1j.xx8ngbg.xwo3gff.x1oyok0e.x1odjw0f.x1e4zzel.x1n2onr6.xq1qtft'
css_selector2 = '.xb57i2i.x1q594ok.x5lxg6s.x78zum5.xdt5ytf.x6ikm8r.x1ja2u2z.x1pq812k.x1rohswg.xfk6m8.x1yqm8si.xjx87ck.xx8ngbg.xwo3gff.x1n2onr6.x1oyok0e.x1odjw0f.x1e4zzel.x5yr21d'
css_selector3 = '.x9f619.x78zum5.x1s65kcs.xixxii4.x13vifvy.xhtitgo.xds687c.x90ctcv.x12dzrxb.xiimyba.xqmrbw9.x1h737yt'
css_selector4 = '.x6s0dn4.x78zum5.x15zctf7.x1s65kcs.x1n2onr6.x1ja2u2z'



# Function to handle the load finished event
def on_load_finished(ok):
    if ok:
        # Inject CSS styles to hide selected elements using JavaScript
        view.page().runJavaScript(f"document.querySelectorAll('{css_selector1}').forEach(el => el.style.display = 'none');")
        view.page().runJavaScript(f"document.querySelectorAll('{css_selector2}').forEach(el => el.style.display = 'none');")
        view.page().runJavaScript(f"document.querySelectorAll('{css_selector3}').forEach(el => el.style.display = 'none');")
        view.page().runJavaScript(f"document.querySelectorAll('{css_selector4}').forEach(el => el.style.display = 'none');")
# Connect the load finished signal to the handler function
view.loadFinished.connect(on_load_finished)

# Show the QWebEngineView window
view.show()

# Start the application event loop
app.exec_()
