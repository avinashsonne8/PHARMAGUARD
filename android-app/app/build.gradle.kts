plugins {
    id("com.android.application")
}

android {
    namespace = "com.pharmaguard.adr"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.pharmaguard.adr"
        minSdk = 23
        targetSdk = 36
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }
}

dependencies {
    implementation("androidx.activity:activity:1.11.0")
    implementation("androidx.appcompat:appcompat:1.7.1")
    implementation("androidx.webkit:webkit:1.15.0")
}
