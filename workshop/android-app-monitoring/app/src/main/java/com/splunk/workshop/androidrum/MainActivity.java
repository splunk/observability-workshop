package com.splunk.workshop.androidrum;

import android.app.Activity;
import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import com.splunk.rum.integration.customtracking.CustomTracking;
import com.splunk.rum.integration.navigation.Navigation;

import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.api.common.Attributes;
import io.opentelemetry.api.trace.Span;
import okhttp3.Call;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends Activity {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private final Handler mainHandler = new Handler(Looper.getMainLooper());
    private final OkHttpClient okHttpClient = new OkHttpClient.Builder().build();

    private LinearLayout logList;
    private TextView currentScreen;
    private int cartItemCount = 0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(buildLayout());

        trackScreen("product_list");
        addLog("App opened on product_list.");
        addLog("RUM configured: " + (InstrumentedShopApplication.isRumConfigured() ? "yes" : "no - pass -PsplunkRumAccessToken"));
        fetchCatalog();
    }

    @Override
    protected void onDestroy() {
        executor.shutdownNow();
        super.onDestroy();
    }

    private View buildLayout() {
        ScrollView scrollView = new ScrollView(this);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(36, 32, 36, 36);
        scrollView.addView(root);

        TextView title = new TextView(this);
        title.setText("Buttercup Android RUM");
        title.setTextSize(26);
        title.setTextColor(Color.rgb(20, 20, 20));
        title.setGravity(Gravity.START);
        root.addView(title);

        TextView subtitle = new TextView(this);
        subtitle.setText("A small shopping flow that shows Splunk RUM instrumentation points.");
        subtitle.setTextSize(15);
        subtitle.setPadding(0, 8, 0, 24);
        root.addView(subtitle);

        currentScreen = new TextView(this);
        currentScreen.setTextSize(18);
        currentScreen.setTextColor(Color.rgb(0, 92, 77));
        currentScreen.setPadding(0, 0, 0, 16);
        root.addView(currentScreen);

        root.addView(button("Open product detail", this::openProductDetail));
        root.addView(button("Add item to cart", this::addToCart));
        root.addView(button("Enter shipping", this::enterShipping));
        root.addView(button("Submit checkout", this::submitCheckout));
        root.addView(button("Track handled payment error", this::trackHandledPaymentError));

        TextView logTitle = new TextView(this);
        logTitle.setText("Instrumentation log");
        logTitle.setTextSize(18);
        logTitle.setPadding(0, 28, 0, 8);
        root.addView(logTitle);

        logList = new LinearLayout(this);
        logList.setOrientation(LinearLayout.VERTICAL);
        root.addView(logList);

        return scrollView;
    }

    private Button button(String label, Runnable action) {
        Button button = new Button(this);
        button.setText(label);
        button.setAllCaps(false);
        button.setOnClickListener(view -> action.run());
        return button;
    }

    private void openProductDetail() {
        trackScreen("product_detail");
        trackEvent("product_detail_viewed", Attributes.of(
                AttributeKey.stringKey("product.category"), "flowers"
        ));
        addLog("Navigation tracked: product_detail.");
    }

    private void addToCart() {
        cartItemCount++;
        trackScreen("cart");
        trackEvent("cart_item_added", Attributes.builder()
                .put("cart.item_count", cartItemCount)
                .put("product.category", "flowers")
                .build());
        addLog("Custom event tracked: cart_item_added. Cart count=" + cartItemCount + ".");
    }

    private void enterShipping() {
        trackScreen("checkout_shipping");
        trackEvent("checkout_step_viewed", Attributes.builder()
                .put("checkout.step", "shipping")
                .put("cart.item_count", cartItemCount)
                .build());
        addLog("Custom event tracked: checkout_step_viewed shipping.");
    }

    private void submitCheckout() {
        trackScreen("checkout_payment");
        addLog("Workflow started: checkout_submit.");

        executor.execute(() -> {
            Span workflow = CustomTracking.getInstance().trackWorkflow("checkout_submit");
            if (workflow != null) {
                workflow.setAttribute("checkout.step", "payment");
                workflow.setAttribute("cart.item_count", cartItemCount);
            }

            try {
                Request request = new Request.Builder()
                        .url("https://httpbin.org/delay/1")
                        .header("Accept", "application/json")
                        .build();
                Call.Factory callFactory = InstrumentedShopApplication.instrumentedCallFactory(okHttpClient);
                try (Response response = callFactory.newCall(request).execute()) {
                    if (workflow != null) {
                        workflow.setAttribute("checkout.http_status", response.code());
                        workflow.setAttribute("checkout.result", response.isSuccessful() ? "success" : "failure");
                    }
                    runOnMain(() -> {
                        trackScreen("confirmation");
                        addLog("Instrumented OkHttp call completed with HTTP " + response.code() + ".");
                        addLog("Workflow ended: checkout_submit.");
                    });
                }
            } catch (IOException e) {
                if (workflow != null) {
                    workflow.setAttribute("checkout.result", "network_error");
                }
                CustomTracking.getInstance().trackException(e, Attributes.of(
                        AttributeKey.stringKey("feature.name"), "checkout"
                ));
                runOnMain(() -> addLog("Handled network exception tracked: " + e.getClass().getSimpleName() + "."));
            } finally {
                if (workflow != null) {
                    workflow.end();
                }
            }
        });
    }

    private void trackHandledPaymentError() {
        IllegalStateException error = new IllegalStateException("Payment method missing");
        CustomTracking.getInstance().trackException(error, Attributes.builder()
                .put("feature.name", "checkout")
                .put("error.recoverable", true)
                .put("checkout.step", "payment")
                .build());
        addLog("Handled exception tracked: Payment method missing.");
    }

    private void fetchCatalog() {
        executor.execute(() -> {
            Request request = new Request.Builder()
                    .url("https://httpbin.org/json")
                    .header("Accept", "application/json")
                    .build();
            Call.Factory callFactory = InstrumentedShopApplication.instrumentedCallFactory(okHttpClient);
            try (Response response = callFactory.newCall(request).execute()) {
                runOnMain(() -> addLog("Catalog API call completed with HTTP " + response.code() + "."));
            } catch (IOException e) {
                CustomTracking.getInstance().trackException(e, Attributes.of(
                        AttributeKey.stringKey("feature.name"), "catalog"
                ));
                runOnMain(() -> addLog("Catalog API exception tracked: " + e.getClass().getSimpleName() + "."));
            }
        });
    }

    private void trackScreen(String screenName) {
        currentScreen.setText("Current screen: " + screenName);
        Navigation.getInstance().track(screenName);
    }

    private void trackEvent(String name, Attributes attributes) {
        CustomTracking.getInstance().trackCustomEvent(name, attributes);
    }

    private void addLog(String message) {
        TextView row = new TextView(this);
        row.setText("- " + message);
        row.setTextSize(14);
        row.setPadding(0, 4, 0, 4);
        logList.addView(row, 0);
    }

    private void runOnMain(Runnable action) {
        mainHandler.post(action);
    }
}
