#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]

def edit(path, transform):
    p = ROOT / path
    if not p.exists():
        raise SystemExit(f"Required upstream file missing: {path}")
    old = p.read_text(encoding="utf-8")
    new = transform(old)
    if new == old:
        raise SystemExit(f"Patch did not change {path}; upstream source may have changed.")
    p.write_text(new, encoding="utf-8")

main_activity = '''package ro.alynsampmobile.launcher;

import android.os.Bundle;
import android.text.InputFilter;
import android.text.InputType;
import android.view.Gravity;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;

import java.io.File;
import java.util.Objects;

import com.joom.paranoid.Obfuscate;
import ro.alynsampmobile.game.SAMP;
import ro.alynsampmobile.launcher.utils.Utils;

@Obfuscate
public class MainActivity extends AppCompatActivity {
    private static final String SERVER_HOST = "142.132.203.47";
    private static final String SERVER_PORT = "16234";
    private static final String LAUNCH_TOKEN = "alynsampmobile1337";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES);

        if (!Objects.equals(getIntent().getStringExtra("extra_check"), LAUNCH_TOKEN)) {
            finish();
            return;
        }

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER);
        root.setPadding(dp(28), dp(28), dp(28), dp(28));
        root.setBackgroundColor(0xFF121212);

        TextView title = new TextView(this);
        title.setText("ALYN SA-MP");
        title.setTextColor(0xFFFFFFFF);
        title.setTextSize(28);
        title.setGravity(Gravity.CENTER);
        title.setTypeface(null, android.graphics.Typeface.BOLD);
        root.addView(title, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView subtitle = new TextView(this);
        subtitle.setText("Enter your nickname");
        subtitle.setTextColor(0xFFBBBBBB);
        subtitle.setTextSize(16);
        subtitle.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams subtitleParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        subtitleParams.topMargin = dp(28);
        root.addView(subtitle, subtitleParams);

        EditText nickname = new EditText(this);
        nickname.setSingleLine(true);
        nickname.setTextSize(18);
        nickname.setTextColor(0xFFFFFFFF);
        nickname.setHintTextColor(0xFF888888);
        nickname.setHint("Nickname");
        nickname.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS);
        nickname.setFilters(new InputFilter[]{new InputFilter.LengthFilter(24)});
        nickname.setText(getSharedPreferences("samp_settings", MODE_PRIVATE)
                .getString("nick_name", ""));
        LinearLayout.LayoutParams inputParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        inputParams.topMargin = dp(12);
        root.addView(nickname, inputParams);

        TextView server = new TextView(this);
        server.setText("Server: " + SERVER_HOST + ":" + SERVER_PORT);
        server.setTextColor(0xFFAAAAAA);
        server.setTextSize(13);
        server.setGravity(Gravity.CENTER);
        LinearLayout.LayoutParams serverParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        serverParams.topMargin = dp(12);
        root.addView(server, serverParams);

        Button play = new Button(this);
        play.setText("PLAY");
        play.setTextSize(16);
        LinearLayout.LayoutParams playParams = new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        playParams.topMargin = dp(28);
        root.addView(play, playParams);

        play.setOnClickListener(v -> {
            String name = nickname.getText().toString().trim();
            if (name.isEmpty()) {
                nickname.setError("Enter your nickname");
                nickname.requestFocus();
                return;
            }

            boolean saved = getSharedPreferences("samp_settings", MODE_PRIVATE).edit()
                    .putString("nick_name", name)
                    .putInt("samp_version", 0)
                    .putBoolean("offline_mode", false)
                    .commit();

            boolean serverSaved = getSharedPreferences("samp_server", MODE_PRIVATE).edit()
                    .putString("host", SERVER_HOST)
                    .putString("port", SERVER_PORT)
                    .putString("password", "")
                    .commit();

            File externalFiles = getExternalFilesDir(null);
            if (!saved || !serverSaved || externalFiles == null) {
                Toast.makeText(this, "Could not save connection settings.", Toast.LENGTH_LONG).show();
                return;
            }

            File sampDirectory = new File(externalFiles, "SAMP");
            if (!sampDirectory.exists() && !sampDirectory.mkdirs()) {
                Toast.makeText(this, "Could not prepare game settings.", Toast.LENGTH_LONG).show();
                return;
            }

            Utils.saveSettings(this);
            File config = new File(sampDirectory, "settings.json");
            if (!config.isFile() || config.length() == 0) {
                Toast.makeText(this, "Could not create game settings.", Toast.LENGTH_LONG).show();
                return;
            }

            try {
                android.content.Intent intent = new android.content.Intent(this, SAMP.class);
                intent.putExtra("extra_check", LAUNCH_TOKEN);
                startActivity(intent);
            } catch (Exception e) {
                Toast.makeText(this, "Could not start SA-MP: " + e.getMessage(),
                        Toast.LENGTH_LONG).show();
            }
        });

        setContentView(root);
    }

    private int dp(float value) {
        return (int) (value * getResources().getDisplayMetrics().density + 0.5f);
    }
}
'''

edit("app/src/main/java/ro/alynsampmobile/launcher/MainActivity.java", lambda _: main_activity)

def patch_app_gradle(s):
    s = s.replace('    id "com.google.gms.google-services"\n', '')
    s = s.replace('    id "com.google.firebase.crashlytics"\n', '')
    s = s.replace('applicationId "ro.alynsampmobile.launcher"', 'applicationId "com.ahhsjdjsjsh.alynautoconnect"')
    s = s.replace('versionName "17.0"', 'versionName "1.0"')
    s = s.replace('    implementation(libs.firebase.analytics)\n', '')
    s = s.replace('    implementation(libs.firebase.crashlytics.ndk)\n', '')
    return s
edit("app/build.gradle", patch_app_gradle)

def patch_root_gradle(s):
    s = s.replace('    id "com.google.gms.google-services" apply false\n', '')
    s = s.replace('    id "com.google.firebase.crashlytics" apply false\n', '')
    return s
edit("build.gradle", patch_root_gradle)

def patch_settings_gradle(s):
    s = s.replace('        classpath "com.google.gms:google-services:4.4.2"\n', '')
    s = s.replace('        classpath "com.google.firebase:firebase-crashlytics-gradle:3.0.3"\n', '')
    return s
edit("settings.gradle", patch_settings_gradle)

def patch_catalog(s):
    s = re.sub(r'^firebaseAnalytics\s*=\s*"[^"]+"\r?\n', '', s, flags=re.M)
    s = re.sub(r'^firebaseCrashlyticsNdk\s*=\s*"[^"]+"\r?\n', '', s, flags=re.M)
    s = re.sub(r'^firebase-analytics\s*=.*\r?\n', '', s, flags=re.M)
    s = re.sub(r'^firebase-crashlytics-ndk\s*=.*\r?\n', '', s, flags=re.M)
    return s
edit("gradle/libs.versions.toml", patch_catalog)

def patch_ui(s):
    s = s.replace('import com.google.firebase.crashlytics.FirebaseCrashlytics;\n', '')
    s = s.replace('        FirebaseCrashlytics.getInstance().setCrashlyticsCollectionEnabled(false);\n', '')
    return s
edit("app/src/main/java/ro/alynsampmobile/game/ui/UI.java", patch_ui)

(ROOT / "app/google-services.json").unlink(missing_ok=True)

strings_path = ROOT / "app/src/main/res/values/strings.xml"
strings = strings_path.read_text(encoding="utf-8")
strings = strings.replace('<string name="app_name">Alyn SA-MP Mobile</string>',
                          '<string name="app_name">Alyn AutoConnect</string>')
strings_path.write_text(strings, encoding="utf-8")

readme = """# Alyn SA-MP AutoConnect

A separate Alyn SA-MP Mobile build configured for one server.

- Nickname prompt: first launcher screen after Alyn's required startup/file check.
- Server: 142.132.203.47:16234 (fixed in the launcher).
- SA-MP protocol: 0.3.7.
- The original National-Street-RP-Launcher repository is not modified.

## Build

Use the Actions tab and run Build Alyn AutoConnect APK, or push a commit to main.
The workflow checks out the pinned Alyn source snapshot, applies the AutoConnect changes, and builds a debug APK. Download alyn-autoconnect-debug from the workflow run's Artifacts section.

## Important

The Alyn client hooks GTA: San Andreas Android 2.10 only. You must have the legitimate compatible GTA SA game data installed/available on the device. This repository does not bundle Rockstar game data. The first Alyn startup may also perform its normal game-file/update checks.

Source snapshot: Fiki-io/alyn-remake, pinned to commit 2cbb0757572a3e17aa6b4da82d6c7fcd4327eeb1.
"""
(ROOT / "README.md").write_text(readme, encoding="utf-8")
print("Alyn AutoConnect patches applied.")
