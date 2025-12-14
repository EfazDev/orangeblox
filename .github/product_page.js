'use strict';
document.addEventListener("DOMContentLoaded", async (ev) => {
    let beta = window.location.host == "obxbeta.efaz.dev";
    let version_req = null;
    let version_json = null;
    let github_repo_info_req = await fetch("https://api.github.com/repos/EfazDev/orangeblox");
    let github_repo_info_json = await github_repo_info_req.json();
    let github_repo_release_info_req = await fetch("https://api.github.com/repos/EfazDev/orangeblox/releases");
    let github_repo_release_info_json = await github_repo_release_info_req.json();
    let github_repo_late_release_info_json = null;

    let stars = 0;
    let total_downloads = 0;
    let latest_downloads = 0;

    if (beta == true) {
        version_req = await fetch("https://obxbeta.efaz.dev/Version.json");
    } else {
        version_req = await fetch("https://obx.efaz.dev/Version.json");
    }
    version_json = await version_req.json()
    if (github_repo_info_req.ok) {
        stars = github_repo_info_json.stargazers_count;
    }
    if (github_repo_release_info_req.ok) {
        for (const release of github_repo_release_info_json) {
            if (!release.assets) continue;
            if (release.assets.length <= 0) continue;
            total_downloads += release.assets.reduce((sum, asset) => sum + asset.download_count, 0);
            if (beta == false && release.prerelease == true) continue;
            if (beta == true && release.prerelease == false) continue;
            if (github_repo_late_release_info_json == null) github_repo_late_release_info_json = release;
            let tr_element = document.createElement("tr");
            tr_element.style = "height: 30px;";
            tr_element.innerHTML = '<td style="height: 30px; width: 30px;"><a href="https://github.com/EfazDev/orangeblox/releases/download/' + release.tag_name + '/OrangeBlox-' + release.tag_name + '.zip">⬇️</a></td><td style="height: 30px; width: 250px;"><a style="color: #ff4b00;" href="https://github.com/EfazDev/orangeblox/releases/download/' + release.tag_name + '/OrangeBlox-' + release.tag_name + '.zip">Download ' + release.tag_name + '</a></td>';
            document.getElementById("old_downloads").append(tr_element);
        }
    }
    if (github_repo_late_release_info_json && github_repo_late_release_info_json.assets) {
        latest_downloads = github_repo_late_release_info_json.assets.reduce((sum, asset) => sum + asset.download_count, 0);
    }
    let stats_ele = document.getElementById("stats");
    stats_ele.innerHTML = '🚀 v' + version_json["latest_version"] + ' (⬇️ ' + latest_downloads.toString() + ') • ⬇️ ' + total_downloads.toString() + ' Downloads (Total) • ⭐ ' + stars.toString() + ' Stars <br><a class="link" href="https://github.com/EfazDev/orangeblox/releases">📦 Releases</a> • <a class="link" href="https://github.com/EfazDev/orangeblox/issues">🛠️ Issues</a> • <a class="link" href="https://github.com/EfazDev/orangeblox/wiki">📕 Wiki</a> • <a class="link" href="https://github.com/EfazDev/orangeblox/pulls">🧲 Pull Requests</a>';
    if (version_req.ok) {
        let download_link_ele = document.getElementById("download_link");
        download_link_ele.href = "https://github.com/EfazDev/orangeblox/releases/download/v" + version_json["latest_version"] + "/OrangeBlox-v" + version_json["latest_version"] + ".zip";
    }
    if (beta == false && document.getElementById("beta_warning")) {
        document.getElementById("beta_warning").remove();
    }
    document.getElementById("releases_btn").addEventListener("click", () => {
        if (document.getElementById("old_downloads").getAttribute("style") == "display: grid;") {
            document.getElementById("old_downloads").style = "display: none;";
            document.getElementById("top_table").style = "display: none;";
        } else {
            document.getElementById("old_downloads").style = "display: grid;";
            document.getElementById("top_table").style = "margin-left: auto; margin-right: auto; height: 54px;";
        }
    });
});
