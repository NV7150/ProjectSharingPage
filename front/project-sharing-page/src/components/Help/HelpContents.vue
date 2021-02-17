<template>
  <v-card>
    <v-card-title>
      <h1>
        SFC21 Project Sharing Port
      </h1>
    </v-card-title>
    <v-divider class="my-3" />
    <v-card-text>
      <h2>はじめに</h2><br>
      <p>
        このサイトは，来季より慶應義塾大学湘南藤沢キャンパス(SFC)へ進学予定のSFC21期生に向けて，現在行っている自主課題や活動を共有するものです。<br>
        SFC21やSFC関係者の方々の積極的な利用をお願いします。<br>
        まだ開発途中のため，バグ報告や要望がありましたら<a href="#contact" class="text-decoration-none">お問い合わせ</a>より管理者にお問い合わせください。
      </p><br>

      <h2>ユーザ登録</h2><br>
      <p>
        ユーザ登録については，<a href="#contact" class="text-decoration-none">お問い合わせ</a>より管理者にお問い合わせください。<br>
        SFC21，SFC関係者の方々であれば大体登録手続きを行います。
      </p><br>

      <h2>使い方</h2><br>
      <h3>ログイン</h3>
      <p>ページ右上の「LOGIN」よりログインできます。</p>

      <h3>ユーザ情報の確認・編集</h3>
      <p>ログイン後，ページ右上のユーザアイコンを押した後に表示されるメニュー（ユーザメニュー）の，「PROFILE」から情報の確認，「EDIT」から編集が行えます。</p>

      <h3>新しいプロジェクトの作成</h3>
      <p>
        ログイン後，ページ右上のユーザメニューの「NEW PROJECT」より新しいプロジェクトを作成できます。<br>
        プロジェクトの作成には，「プロジェクト名」，「プロジェクトの概要」，「プロジェクトの説明」，「プロジェクトを表す画像」が必要になります。<br>
        また，任意で「プロジェクトに関連するタグ」，「プロジェクトに関連するSNS」の登録が行えます。
      </p>

      <h3>プロジェクトページ</h3>
      <p>
        プロジェクトページでは，「プロジェクトの情報の確認」と「チャット」が行えます。<br>
        また，「JOIN THIS PROJECT」を押すことで，プロジェクトへの参加申請を管理者に送ることができます。<br>
        管理者は，「プロジェクト情報の編集」と「メンバー情報の管理」を行えます。
      </p>
      <h4>メンバーの権限</h4>
      <v-simple-table>
        <tbody>
          <tr v-for="(item, i) in members" :key="i">
            <td>{{item.name}}</td>
            <td>{{item.description}}</td>
          </tr>
        </tbody>
      </v-simple-table><br>
      <h4>チャットの種類</h4>
      <v-simple-table>
        <tbody>
        <tr v-for="(item, i) in chats" :key="i">
          <td>{{item.name}}</td>
          <td>{{item.description}}</td>
        </tr>
        </tbody>
      </v-simple-table><br><br>

      <h2>お願い</h2><br>
      <p>
        ある程度利用していただいたら自主課題のための<a href="https://forms.gle/tftxLqj9Lp5cmGBv6" class="text-decoration-none">アンケート</a>にご協力をお願いします。<br>
      </p><br>


      <h2 id="contact">お問い合わせ</h2><br>
      <p>
        <router-link
            :to="{name: 'UserPage', params: { userName: 'publicClassMain' }}"
            class="text-decoration-none"
        >
          だんご
        </router-link><br>
        <router-link
            :to="{name: 'UserPage', params: { userName: 'kekeho' }}"
            class="text-decoration-none"
        >
          kekeho
        </router-link>
      </p>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "HelpContents",
  data(){
    return{
      members: [
        {
          name: "Member",
          description: "プロジェクトのメンバーです。プロジェクトページにプロフィールが関連付けられます。"
        },
        {
          name: "Advanced Member",
          description: "プロジェクトメンバーの中でも，特別なチャットに書き込みを行えます。"
        },
        {
          name: "Admin",
          description: "プロジェクトの管理者です。プロジェクトの編集，メンバーの承認・権限変更等を行えます。一度ADMINに指定すると解任できません。"
        }
      ],
      chats: [
        {
          name: "OpenChat",
          description: "誰でもスレッドを作成でき，誰でも書き込みが行えます。"
        },
        {
          name: "Announce",
          description: "Advanced Member以上がスレッドの作成と書き込みが行えます。"
        },
        {
          name: "Problems",
          description: "Member以上がスレッドを作成でき，誰でも書き込みが行えます。"
        }
      ]
    };
  }
}
</script>

<style scoped>

</style>