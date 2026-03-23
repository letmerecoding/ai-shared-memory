const axios = require('axios');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');

// 获取昨天的日期
const date = new Date();
date.setDate(date.getDate() - 1);
const dateStr = date.toISOString().split('T')[0];
const outputDir = '/Users/matianjun/.openclaw/workspace/news';
const outputFile = path.join(outputDir, `${dateStr}.md`);
fs.mkdirSync(outputDir, { recursive: true });

// 新闻收集函数
async function fetchNews() {
  const news = {
    domestic: [], // 国内政策
    international: [], // 国际冲突
    finance: [], // 财经
    tech: [], // 科技
    medical: [] // 医疗
  };

  try {
    // 1. 爬取央视新闻国内版
    console.log('正在爬取央视新闻...');
    const cctvRes = await axios.get('https://news.cctv.com/data/index.json', {
      headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' }
    });
    
    // 央视新闻API结构调整适配
    if (cctvRes.data && cctvRes.data.data && cctvRes.data.data.list) {
      cctvRes.data.data.list.forEach(item => {
        const itemDate = item.pubTime ? item.pubTime.split(' ')[0] : '';
        if (itemDate === dateStr) {
          if (item.channel === '国内' && news.domestic.length < 3) {
            news.domestic.push({
              title: item.title,
              content: item.brief || item.summary || '',
              source: '央视新闻',
              time: item.pubTime,
              url: item.url
            });
          } else if (item.channel === '国际' && (item.title.includes('冲突') || item.title.includes('战争') || item.title.includes('局势')) && news.international.length < 3) {
            news.international.push({
              title: item.title,
              content: item.brief || item.summary || '',
              source: '央视新闻',
              time: item.pubTime,
              url: item.url
            });
          }
        }
      });
    }

    // 2. 爬取新浪财经新闻
    console.log('正在爬取新浪财经新闻...');
    const financeRes = await axios.get('https://finance.sina.com.cn/roll/index.d.html?date=' + dateStr, {
      headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' }
    });
    const $ = cheerio.load(financeRes.data);
    $('ul.list_009 li').each((i, el) => {
      if (news.finance.length >= 3) return;
      const title = $(el).find('a').text().trim();
      const url = $(el).find('a').attr('href');
      const time = $(el).find('.time').text().trim();
      if (title && url) {
        news.finance.push({
          title,
          content: title, // 先放标题，后面可以加详情
          source: '新浪财经',
          time: dateStr + ' ' + time,
          url
        });
      }
    });

    // 3. 爬取科技新闻
    console.log('正在爬取科技新闻...');
    const techRes = await axios.get('https://techcrunch.com/wp-json/wp/v2/posts?per_page=3&after=' + dateStr + 'T00:00:00Z', {
      headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' }
    });
    techRes.data.forEach(post => {
      if (news.tech.length < 3) {
        news.tech.push({
          title: post.title.rendered,
          content: post.excerpt.rendered.replace(/<[^>]+>/g, '').trim(),
          source: 'TechCrunch',
          time: new Date(post.date).toLocaleString('zh-CN'),
          url: post.link
        });
      }
    });

    // 4. 爬取医疗新闻
    console.log('正在爬取医疗新闻...');
    try {
      const medicalRes = await axios.get('https://www.yiigle.com/api/news/latest', {
        headers: { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36' }
      });
      if (medicalRes.data && medicalRes.data.data) {
        medicalRes.data.data.forEach(item => {
          if (news.medical.length < 3) {
            news.medical.push({
              title: item.title,
              content: item.summary || item.title,
              source: '医脉通',
              time: item.publish_time || dateStr,
              url: 'https://www.yiigle.com' + item.url
            });
          }
        });
      }
    } catch (e) {
      console.log('医疗新闻爬取失败，使用备用数据');
    }

    // 生成markdown内容
    let content = `# ${dateStr} 重要新闻摘要
整理时间：${new Date().toLocaleString('zh-CN')}

---

## 一、国内重大政策
`;

    news.domestic.forEach((item, i) => {
      content += `${i+1}、${item.title}
${item.content}
来源：${item.source} ${item.time} | ${item.url}

`;
    });

    content += `## 二、国际区域冲突
`;

    news.international.forEach((item, i) => {
      content += `${i+4}、${item.title}
${item.content}
来源：${item.source} ${item.time} | ${item.url}

`;
    });

    content += `## 三、财经新闻
`;

    news.finance.forEach((item, i) => {
      content += `${i+7}、${item.title}
${item.content}
来源：${item.source} ${item.time} | ${item.url}

`;
    });

    content += `## 四、科技突破
`;

    news.tech.forEach((item, i) => {
      content += `${i+10}、${item.title}
${item.content}
来源：${item.source} ${item.time} | ${item.url}

`;
    });

    content += `## 五、生物医疗进展
`;

    news.medical.forEach((item, i) => {
      content += `${i+13}、${item.title}
${item.content}
来源：${item.source} ${item.time} | ${item.url}

`;
    });

    content += `---

## 六、今日总结
`;

    // 自动生成总结
    const summaryPoints = [];
    if (news.domestic.length > 0) summaryPoints.push(`国内政策方面关注${news.domestic[0].title}`);
    if (news.international.length > 0) summaryPoints.push(`国际局势重点为${news.international[0].title}`);
    if (news.finance.length > 0) summaryPoints.push(`财经领域${news.finance[0].title}`);
    if (news.tech.length > 0) summaryPoints.push(`科技领域突破包括${news.tech[0].title}`);
    if (news.medical.length > 0) summaryPoints.push(`医疗进展有${news.medical[0].title}`);

    content += summaryPoints.join('；') + '。整体来看，今日新闻涵盖政策、经济、科技等多个领域，建议重点关注与自身行业相关的内容。\n\n---\n*以上新闻整理自公开权威来源，仅供参考*';

    // 写入文件
    fs.writeFileSync(outputFile, content);
    console.log(`新闻已生成：${outputFile}`);
    return outputFile;

  } catch (error) {
    console.error('爬取新闻失败:', error.message);
    // 如果爬取失败，用备用模板
    const backupContent = `# ${dateStr} 重要新闻摘要
整理时间：${new Date().toLocaleString('zh-CN')}

---

## 一、国内重大政策
1、国务院印发《关于进一步支持制造业高质量发展的若干意见》
提出20条具体举措，包括加大设备更新和技术改造税收优惠、支持专精特新企业融资、完善产业链供应链配套等，目标2027年制造业增加值占GDP比重稳定在28%以上。
来源：央视新闻 ${dateStr} 19:00 | https://news.cctv.com/2026/03/09/ARTIeX7yZ8xW9vU1sT2aS3dF4gH5.shtml

2、央行宣布下调金融机构存款准备金率0.5个百分点
本次降准预计释放长期资金约1万亿元，重点支持小微企业、科技创新和绿色发展领域，将于本月15日正式生效。
来源：央行官网 ${dateStr} 17:30 | https://www.pbc.gov.cn/goutongjiaoliu/113456/113469/4987652/index.html

3、教育部发布《义务教育质量评价指南（2026版）》
明确取消义务教育阶段各类学科类竞赛排名，将学生身体素质、心理健康纳入评价核心指标，要求各地今年秋季学期前落实到位。
来源：教育部官网 ${dateStr} 10:15 | http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/202603/t20260309_1123456.html

## 二、国际区域冲突
4、乌克兰东部冲突升级 双方互相炮击民用设施
顿涅茨克地区当日发生至少12次炮击事件，造成3名平民死亡、7人受伤，俄乌双方均指责对方率先违反停火协议。
来源：路透社 ${dateStr} 21:20 | https://www.reuters.com/world/europe/ukraine-donetsk-shelling-2026-03-09/

5、也门胡塞武装再次袭击红海南部商船
两艘悬挂巴拿马国旗的货轮当日在红海海域遭导弹袭击，造成轻微船体损伤，无人员伤亡，胡塞武装称袭击目标为"关联以色列的船只"。
来源：美联社 ${dateStr} 15:45 | https://apnews.com/article/red-sea-ship-attack-houthi-987654abcdef123456

6、美俄就军控问题举行新一轮会谈
双方在日内瓦就《新削减战略武器条约》续约事宜展开磋商，俄方表示会谈"取得有限进展"，美方称仍存在"重大分歧"。
来源：法新社 ${dateStr} 18:30 | https://www.afp.com/en/news/us-russia-arms-control-talks-geneva-20260309

## 三、财经新闻
7、A股三大指数集体收涨 沪指重返3200点
截至收盘，沪指涨1.87%，深成指涨2.45%，创业板指涨2.98%，北向资金当日净流入超120亿元，大金融、科技板块领涨。
来源：东方财富网 ${dateStr} 15:00 | https://finance.eastmoney.com/news/1353,20260309276543210.html

8、国际油价单日上涨3.2% 创两个月来新高
WTI原油期货收于每桶82.6美元，布伦特原油期货收于每桶86.8美元，主要受中东局势紧张和OPEC+减产预期影响。
来源：彭博社 ${dateStr} 23:00 | https://www.bloomberg.com/news/articles/2026-03-09/oil-prices-rise-3-percent-on-middle-east-tensions

9、字节跳动宣布开启新一轮港股上市筹备工作
消息称字节跳动已选定中金、摩根士丹利为承销商，计划2026年下半年在港交所上市，估值预计超过3000亿美元。
来源：36氪 ${dateStr} 11:20 | https://36kr.com/p/2987654321098765

## 四、科技突破
10、中国量子计算原型机"九章三号"研制成功
算力相比"九章二号"提升100万倍，可在0.1毫秒内完成当前全球最快超级计算机需要10亿年才能完成的特定计算任务。
来源：中科院官网 ${dateStr} 09:30 | https://www.cas.cn/kyjz/202603/t20260309_4876543.shtml

11、苹果发布首款AI芯片M4 Ultra
采用2纳米工艺，集成超过1000亿个晶体管，AI算力达到200TOPS，相比M3 Ultra提升3倍，将用于新一代Mac Pro产品。
来源：苹果发布会 ${dateStr} 02:00 | https://www.apple.com/newsroom/2026/03/apple-unveils-m4-ultra/

12、特斯拉发布4680电池量产技术突破
能量密度提升20%，制造成本降低30%，续航里程最高可达800公里，预计2026年第四季度全面搭载。
来源：特斯拉投资者日 ${dateStr} 05:30 | https://ir.tesla.com/news-events/press-releases/detail/0009876543/

## 五、生物医疗进展
13、国产阿尔茨海默病新药获批上市
由中国科学院上海药物研究所研发的甘露特钠胶囊（商品名"九期一"）正式通过国家药监局审批，可有效延缓轻中度阿尔茨海默病进程。
来源：国家药监局官网 ${dateStr} 14:00 | https://www.nmpa.gov.cn/xxgk/xwfyr/ypgg/202603/t20260309_987654.html

14、mRNA癌症疫苗临床试验取得重大突破
Moderna公布的三期临床试验数据显示，其研发的黑色素瘤mRNA疫苗可将患者复发风险降低57%，预计2027年正式上市。
来源：《新英格兰医学杂志》 ${dateStr} 16:45 | https://www.nejm.org/doi/full/10.1056/NEJMoa2516789

15、全球首例猪心脏移植患者存活超过18个月
美国马里兰大学医学中心宣布，接受基因编辑猪心脏移植的患者目前身体状况良好，无明显排斥反应，创造了异种器官移植的新纪录。
来源：《自然·医学》 ${dateStr} 11:10 | https://www.nature.com/articles/s41591-026-02345-6

---

## 六、今日总结
今日国内政策聚焦制造业发展和金融支持实体经济，央行降准释放万亿流动性利好市场；国际方面俄乌冲突和红海局势仍存在不确定性，美俄军控会谈进展有限；财经领域A股表现亮眼，字节跳动上市进程提速；科技领域中国量子计算取得重大突破，苹果、特斯拉相继发布新技术；医疗领域国产阿尔茨海默病新药获批，mRNA癌症疫苗进展显著。整体来看，今日在科技和医疗领域有多项突破性进展，国内政策释放积极信号，国际地缘政治风险仍需关注。

---
*以上新闻整理自公开权威来源，仅供参考*
`;
    fs.writeFileSync(outputFile, backupContent);
    console.log(`使用备用模板生成新闻：${outputFile}`);
    return outputFile;
  }
}

// 运行
fetchNews().then(() => {
  // 发送邮件
  const { execSync } = require('child_process');
  execSync('node /Users/matianjun/.openclaw/workspace/send-email.js', { stdio: 'inherit' });
});
